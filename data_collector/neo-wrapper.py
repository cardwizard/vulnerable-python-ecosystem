from neo4j import GraphDatabase

port = 7688
data_uri = 'bolt://localhost:' + str(port)

username = 'neo4j'
password = 'abc123'
# data_creds = (username, password)
data_creds = None

driver = GraphDatabase.driver(data_uri, auth=data_creds)

def close_db():
    driver.close()

def clear_db():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    print("Cleared graph.")

"""
@param pkg_data : Python dictionary of package data to be inserted
"""

def push_pkg(pkg_data):

    name = pkg_data['name']
    #maintainer_info = (pkg_data['main_name'], pkg_data['main_email'])
    #author_info = pkg_data['auth_name'], pkg_data['auth_email'])

    maintainer_info = pkg_data['maintainer_email']
    author_info = pkg_data['author_email']
    downloads = pkg_data['downloads']
    lic = pkg_data['license']
    version = pkg_data['version']
    dependences = pkg_data['dep_list']

    with driver.session() as session:
        result = session.run("MATCH (n:Package {name: $name}) RETURN id(n)", name=name).single()
        
        if result == None:
            result = session.run("CREATE (n:Package {name: $name," 
                "main_email:$main_emailauth_email:$auth_email, version: $version"
                "downloads: $downloads, license: $license}) RETURN id(n)",
                name=name,
                main_email=maintainer_info,
                auth_email=author_info, version=version,
                downloads=downloads, license=lic).single().value()
        else:
            pkg_id = result.value()

            session.run("MATCH (n:Package) WHERE id(n) = $pkg_id "
                    "SET n.main_email = $main_email "
                    "SET n.auth_email = $auth_email "
                    "SET n.version = $version"
                    "SET n.downloads = $downloads "
                    "SET n.license = $license",
                pkg_id=pkg_id,
                main_email=maintainer_info,
                auth_email=author_info,
                version=version,
                downloads=downloads, license=lic
            )

        for dep in dependences:
            if dep == "UNKNOWN":
                continue   
            
            try:
                #dep_id = session.run("MATCH (n:Package {name: $name}) RETURN id(n)", name=dep).single()
                #session.run("MERGE (n:Package {name: $name})-[:REQURES]->(m:Package {name: $mname})", name=name, mname=dep)
            
                session.run("MATCH (n:Package {name: $name}) "
                    "MERGE (m:Package {name: $depname}) "
                    "MERGE (n)-[:REQUIRES]->(m)",
                    name=name, depname=dep)
            
            except Exception as e:
                print("Exception", e.__str__())

def get_dependency_counts(packages):
    dep_counts = [0] * len(packages)

    with driver.session() as session:

        for i, pkg_name in tqdm(enumerate(packages)):
       
            result = session.run("match (n {name: $name})<-[*1..]-(dst) return count(distinct dst)", name=pkg_name).single()

            if result == None:
                continue
            else:
                dep_counts[i] = result.value()

    return dep_counts
        
if __name__ == '__main__':
    print("Running tests for neo-wrapper.")

    clear_db()

    pkg1 = {
        "name": "pack3",
        "main_name": "Josh",
        "main_email": "Josh@email.com",
        "auth_name": "Aadesh",
        "auth_email": "Aadesh@email.com",
        "downloads": 30,
        "license": "Apache v2.0",
        "dep_list": ["packone", "packtwo"]
    }

    push_pkg(pkg1)

    pkg2 = {
        "name": "testpack",
        "main_name": "Jane",
        "main_email": "Jane@email.com",
        "auth_name": "Aadesh",
        "auth_email": "Aadesh@email.com",
        "downloads": 20,
        "license": "Apache v2.0",
        "dep_list": ["pack3", "packtwo"]
    }

    push_pkg(pkg2)

    pkg3 = {
        "name": "packtwo",
        "main_name": "Mike",
        "main_email": "Jike@email.com",
        "auth_name": "Heather",
        "auth_email": "Heather@email.com",
        "downloads": 20,
        "license": "Apache v2.0",
        "dep_list": []
    }

    push_pkg(pkg3)

    close_db()

    print("Done.")


