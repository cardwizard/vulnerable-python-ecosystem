# A Study of Security Vulnerabilities in the Python Ecosystem
The popularity of Python has lead to a large ecosystem of third-party packages available via the pip software package registry. The open nature of pip has boosted its growth, providing over 100,000 free and reusable software packages. 
We wish to study the security risks for users of pip by systematically analyzing dependencies between packages, the maintainers responsible for these packages, and publicly reported security issues. 
We wish to answer certain questions and identify potential threats caused due to heavy code reuse in the Python ecosystem. We plan on building a dependency graph of all packages we can scrape from pypi.org and analyze things like:  
 - How big is the blast radius for certain packages? In case a particular package is hacked / there is malicious code in a certain package, how big would the impact be?  
 - Is it possible to identify typo-squatting attempts in the ecosystem.
 - Can we identify license violations?
 - How big of an impact would hacking the account of a particular maintainer create?
 - Can we give a security rating to a particular package based on how quickly they patch identified vulnerabilities, etc.?
    
## Background and Related Work
Other cloud-based repository environments that have been studied previously include npm for Javascript packages and Docker Hub for container images.  
__“Small World with High Risks: A Study of Security Threats in the npm Ecosystem”__ (link)  

This study of the npm ecosystem showed that:
 - Users implicitly trust and install around 80 other packages on average when installing one npm package.
 - Some of the most popular packages can reach more than 100,000 other packages. 
 - Only 391 influential maintainers affect more than 10,000 packages.

__“A Study of Security Vulnerabilities on Docker Hub” (link)__
This study of Docker Hub showed that:
 - There are 180 vulnerabilities on average number for all versions of an image, while even the latest official images have about 70 vulnerabilities on average.
 - 50% of both community and official images have not been updated within 200 days, and 30% of those images have not been updated in 400 days.
 - Child images inject 20 vulnerabilities while also inheriting about 80 vulnerabilities from their parent images.

__“Twelve Malicious Python libraries found and removed from PyPI” (Link)__
 - This article exemplifies our concerns for Python because 10 of the packages listed are clear typosquatting attempts on other popular packages. The attacks in this article leads us to ask further questions about the typosquatting in Python like:
 - How many maintainers are making packages that typosquat other packages?
 - What are other typo squatting attempts targeting?



    

