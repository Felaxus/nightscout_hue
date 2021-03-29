*************************************************
How to set-up the nightscout-phillips integration
*************************************************

| This project is made to display the insulin level of a pump controlled via nighscout. Adjusting the light of the room depending on what you set your environment variables.

Setting up
==========
Firstly, as per hosting there are multiple ways, due to the way this is built, a virtual private server isn't available
YET, however I plan on adding that feature soon. So at the moment the best way to host this is locally or with a `raspberry pi <https://www.raspberrypi.org>`_.

Installing docker
^^^^^^^^^^^^^^^^^

Open a command prompt and download docker and docker-compose. To install docker on a raspberry pi follow `this <https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script>`_
or `this article <https://phoenixnap.com/kb/docker-on-raspberry-pi>`_. Furthermore if you want to install docker on any other
platform to host locally this can obviously be achieved by going `here <https://docs.docker.com/get-docker/>`_ and
following the instructions.

Installing docker-compose
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    sudo apt update
    sudo apt install python3 idle3
    pip install docker-compose


After downloading docker & docker-compose it's time to download the code from github

.. code-block::

    git clone https://github.com/Felaxus/nightscout_hue.git
    cd nightscout_hue
    # Now we have to edit the docker-compose file, you can either use nano or vi.
    # For the simplicity's sake we'll use nano
    nano docker-compose.yml

Editing docker-compose.yml
^^^^^^^^^^^^^^^^^^^^^^^^^^
The `docker-compose.yml <https://github.com/Felaxus/nightscout_hue/blob/main/docker-compose.yml>`_ should look something like this

.. code-block:: yaml

    version: "3.3"

    services:
      main:
        build: .
        container_name: "nightscout_integration"
        environment:
          - PYTHONUNBUFFERED=1
          - NIGHTSCOUT_URL=NONE
          - PHILLIPS_IP=NONE
          - PHILLIPS_USERNAME=NONE
          - BRIGHTNESS_LEVEL=NONE
          - LIGHT_ID=NONE
          - HIGH_COLOR=NONE
          - HIGH_GLUCOSE_VALUE=NONE
          - RANGE_COLOR=NONE
          - LOW_COLOR=NONE
          - LOW_GLUCOSE_VALUE=NONE
          - START_TIME=NONE
          - END_TIME=NONE
          - TIMEZONE_DIFFERENCE=NONE
          - REFRESH_RATE=NONE
          - NIGHTSCOUT_REALTIME_DIFFERENCE=NONE
          - LOCAL_MODE=NONE
          - TOKEN=NONE

You are interested in editing everything under environment, I will explain what to edit each value too and how to
edit it below

.. topic:: NIGHTSCOUT_URL

    This is the url of your heroku or wherever you host nightscout. An example would be https://https://hello.herokuapp.com

.. topic:: PHILLIPS_IP

    The ip of the phillips hue, to get this go `over here <https://discovery.meethue.com/>`_ and you'll find the IP adress


