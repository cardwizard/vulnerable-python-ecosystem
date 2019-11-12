from neo4j import GraphDatabase

from json import load, loads

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
    dependences = pkg_data['dep_list']

    with driver.session() as session:
        result = session.run("MATCH (n:Package {name: $name}) RETURN id(n)", name=name).single()
        
        print(result)

        if result == None:
            print("Result was none")
            result = session.run("CREATE (n:Package {name: $name," 
                "main_name: $main_name, main_email:$main_email, auth_name:$auth_name, auth_email:$auth_email,"
                "downloads: $downloads, license: $license}) RETURN id(n)",
                name=name,
                main_name=maintainer_info[0], main_email=maintainer_info[1],
                auth_name=author_info[0], auth_email=author_info[1],
                downloads=downloads, license=lic).single().value()
        else:
            pkg_id = result.value()
            print("Adding info to package with id ", pkg_id)

            session.run("MATCH (n:Package) WHERE id(n) = $pkg_id "
                    "SET n.main_name = $main_name "
                    "SET n.main_email = $main_email "
                    "SET n.auth_name = $auth_name "
                    "SET n.auth_email = $auth_email "
                    "SET n.downloads = $downloads "
                    "SET n.license = $license",
                pkg_id=pkg_id,
                main_name=maintainer_info[0], main_email=maintainer_info[1],
                auth_name=author_info[0], auth_email=author_info[1],
                downloads=downloads, license=lic
            )

        for dep in dependences:
            if dep == "UNKNOWN":
                continue   
            
            try:
                print("Added dep: ", dep)

                #dep_id = session.run("MATCH (n:Package {name: $name}) RETURN id(n)", name=dep).single()
                #session.run("MERGE (n:Package {name: $name})-[:REQURES]->(m:Package {name: $mname})", name=name, mname=dep)
            
                session.run("MATCH (n:Package {name: $name}) "
                    "MERGE (m:Package {name: $depname}) "
                    "CREATE (n)-[:REQUIRES]->(m)",
                    name=name, depname=dep)
            
            except Exception as e:
                print("Exception", e.__str__())

        
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


