from setuptools import setup, find_packages

setup(
    name="Food-Spoilage-Detector",
    version="0.1.0",
    author="KumudithaSilva",
    author_email="kumudithasilva66@gmail.com",
    description="Early stage food spoilage detection",
    long_description=open("README.md").read(),
    long_description_content_type="",
    maintainer= "kumuditha",
    maintainer_email= "kumudithasilva66@gmail.com",
    url= "https://github.com/KumudithaSilva/mlflow-dvc-food-spoilage-detector",
    project_url ={
        "Bug_Tracker" : "https://github.com/KumudithaSilva/mlflow-dvc-food-spoilage-detector/issues"
    },
    package_dir={"": "src"},
    packages= find_packages(where="src")
)