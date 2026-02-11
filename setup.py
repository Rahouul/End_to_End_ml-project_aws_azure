from setuptools import find_packages, setup
from typing import List


HYPHERN_E_DOT = '-e .'
def get_requirements(file_path:str)-> List[str]:
        """
        this function will return the list of requuiurements
        
        """
        requirements = []
        with open(file_path) as file_obj:
            requirements = file_obj.readlines()
            requirements = [req.replace('\n', '' )for req in requirements]
            
            if HYPHERN_E_DOT in requirements:
                requirements.remove(HYPHERN_E_DOT)
                
        return requirements
#consider this file as metadata of the project
setup(
      name = "E2E_ml_project",
      version= '0.0.1',
      author= "Rahul",
      author_email= 'rrana8227@gmail.com',
      packages= find_packages(),
      #install_requires = ['pandas', 'numpy', 'seaborn']# not feasible when their are many packages
      install_requires = get_requirements('requirements.txt')
      
       
      )