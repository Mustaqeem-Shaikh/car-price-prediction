from setuptools import setup, find_packages

setup(
    name="car price pred",
    version='0.1.0',
    find_packages=find_packages(),
    install_requires=[
        "pandas",
        'numpy',
        'scikit-learn',
        'pyyaml',
        'python-dotenv',
        'boto3',
        'Flask'
    ],
    
    entry_point={
        'console_scripts':[
            "car-train=src.Car.pipelines.training_pipeline:start_training"
            ]
    }
)