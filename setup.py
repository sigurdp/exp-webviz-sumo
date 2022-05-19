from setuptools import setup, find_packages

setup(
    name="exp-webviz-sumo",
    description="Experiments with Sumo in Webviz plugins",
    packages=find_packages(),
    entry_points={
        "webviz_config_plugins": [
            "ListSurfacesPlugin = exp_webviz_sumo:ListSurfacesPlugin",
        ]
    },
    install_requires=[
        "webviz-config",
        #"fmu-sumo@git+https://github.com/equinor/fmu-sumo@e06ece8f6fd674bd6daf7ab31e0ec2fee27ebcbe",
        "fmu-sumo@git+https://github.com/equinor/fmu-sumo@explorer",
        "sumo-wrapper-python@git+https://github.com/equinor/sumo-wrapper-python.git@master",
        "deprecated"
    ],
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    project_urls={
        "Source": "https://github.com/sigurdp/exp-webviz-sumo",
    },
)
