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
          - HIGH_GLUCOSE_VALUE=NONE
          - HIGH_COLOR=NONE
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

    This is the url of your heroku or wherever you host nightscout. An example would be https://hello.herokuapp.com

.. topic:: PHILLIPS_IP

    The ip of the phillips hue, to get this go `over here <https://discovery.meethue.com/>`_ and you'll find the IP adress

.. topic:: PHILLIPS_USERNAME

    The weird token-looking username you created earlier when setting up hue bridge api, scroll up

.. topic:: BRIGHTNESS_LEVEL

    The brightness you want the bulb to power up to, between 1-250

.. topic:: LIGHT_ID

    The light ID or IDs you want to change, we covered this eariler up. If you want to include more than 1 separate them with a comma. Example: 1,2 this would trigger lights 1 and 2

.. topic:: HIGH_GLUCOSE_VALUE

    The value that the code considers high. For example if this is 200, anything more than 200 is considered HIGH.

.. topic:: HIGH_COLOR

    The color the light should turn if the glucose level is higher than HIGH_GLUCOSE_VALUE. You assign one of 5 colors
    the available colors are RED, ORANGE, GREEN, BLUE, PURPLE

.. topic:: LOW_GLUCOSE_VALUE

    The value that the code considers low. For example if this is 90, anything lower than 90 is considered LOW.

.. topic:: LOW_COLOR

    The color the light should turn if the glucose level is lower than LOW_GLUCOSE_VALUE. You assign one of 5 colors
    the available colors are RED, ORANGE, GREEN, BLUE, PURPLE

.. topic:: RANGE_COLOR

    If color is in range, not higher than HIGH_GLUCOSE_VALUE and no lower than LOW_GLUCOSE_VALUE it will turn to this color
    the available colors are RED, ORANGE, GREEN, BLUE, PURPLE

.. topic:: START_TIME

    This is basically from when the light starts, what do I mean by this. Well basically you will have a start
    time and an end_time, basically it will start transmitting light at start time and after end_time it will turn
    lights off until start_time. An example would be ``8:00``, making start time 8 AM

.. topic:: END_TIME

    This is basically from when the light ends, what do I mean by this. Well basically you will have a start
    time and an end_time, basically it will start transmitting light at start time and after end_time it will turn
    lights off until end_time. Beware your end_time cant be for example 1 AM. Maximum is ```23:59``

.. topic:: TIMEZONE_DIFFERENCE

    The difference in time zone with GMT, for example if you have 2 more hours than GMT you'd put ``+2``, if
    you had 2 less hours than GMT you'd put ``-2``

.. topic:: REFRESH_RATE

    How many seconds it checks. For example if you put ``60`` It'd check the glucose level each 60 seconds (1 minute)

.. topic:: NIGHTSCOUT_REALTIME_DIFFERENCE

    The maximum time it allows of intransmission. For example, if the difference between the time now and the time
    nightscout checked is bigger than the number of minutes specified here then it would throw DELAY_COLOR

.. topic:: DELAY_COLOR

    The color to put if NIGHTSCOUT_REALTIME_DIFFERENCE happens, available colors are RED, ORANGE, GREEN, BLUE, PURPLE

.. topic:: LOCAL_MODE

    Coming soon

.. topic:: TOKEN

    Coming soon

Running the script
^^^^^^^^^^^^^^^^^^

Last step is to actually run this, docker-compose makes this very simple just do

.. code-block::

    docker-compose up -d --build --remove-oprhans

**Congrats, it should be working!**

