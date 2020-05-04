# Energy reporting management platform - ERMP

![Logo UCM](https://www.ucm.es/data/cont/docs/60-2018-03-15-LogoBibliotecaucm.png)


ERMP is a platform that manages different reports on energy consumption. The information framework is specified in the Complutense University of Madrid and its energy consumption. Provides energy experts with software capable of:

- Manage roles and security of the platform so that it is specified which people access what data.
- Simple and intuitive web application that allows information to be easily found.
- A detailed analysis of different sections of consumption, focused on the use of photovoltaic panels and everything around it, such as batteries, number of panels, angles...

This project is established on the framework of the end of degree work of the Faculty of Informatics of the Complutense University of Madrid of the academic year 2019/2020. In particular on the career of Software Engineering.

## Instructions

In order to launch the project locally, docker containers are used, an environment has been prepared for its launch and use of dependencies in an easy and simple way.

To start the project, a script has been created that starts everything necessary for its use. The first thing to do:

``` bash
$ ./up.sh
```

When it is finished working or using the platform, it is necessary to remove the running containers. For that it is launched:

``` bash
$ ./down.sh
```

You can check if it works by going to the web:

Web local: [http://localhost:8000/](http://localhost:8000/)

Or by launching docker commands like the following commands and see if you have the containers running:

- Delete container:
    ```
    docker kill <container name>
    ```

- List of containers running:
    ```
    docker ps -a
    ```

- Connect to a running container:
    ```
    docker exec -i -t <container name> /bin/bash
    ```

## Data

The data is drawn from two main sources:

- Consumption sensors from the Complutense University of Madrid.

- Photovoltaic energy information from the European website: [PHOTOVOLTAIC GEOGRAPHICAL INFORMATION SYSTEM](https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html)

## Authors

- Alberto Pastor Moreno:
    - [Github](https://github.com/albertopastormr)
    - [Linkedin](https://www.linkedin.com/in/albertopastormr/)

- Iván Fernández Mena:
    - [Github](https://github.com/ivanfermena)
    - [Linkedin](https://www.linkedin.com/in/ivanfermena/)

## Contributing

## Licence