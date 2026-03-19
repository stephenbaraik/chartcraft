from setuptools import setup, find_packages

setup(
    name="chartcraft",
    version="0.1.0",
    description="Python-powered dashboards that rival Power BI & Tableau.",
    author="stephenbaraik",
    author_email="stephenbaraik@gmail.com",
    url="https://github.com/stephenbaraik/chartcraft",
    packages=find_packages(),
    package_data={
        "chartcraft": [
            "static/*.html",
            "static/*.css",
            "static/*.js",
            "builder/*.html",
            "builder/components/*.js",
            "templates/*.py",
        ]
    },
    python_requires=">=3.11",
    install_requires=[],        # zero required deps — stdlib only
    extras_require={
        "sql":    ["sqlalchemy>=2.0"],
        "pg":     ["sqlalchemy>=2.0", "psycopg2-binary"],
        "mysql":  ["sqlalchemy>=2.0", "pymysql"],
        "mssql":  ["sqlalchemy>=2.0", "pyodbc"],
        "pandas": ["pandas>=1.5"],
        "pdf":    ["playwright>=1.40"],
        "full":   ["sqlalchemy>=2.0", "psycopg2-binary", "pymysql", "pandas>=1.5", "playwright>=1.40"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
