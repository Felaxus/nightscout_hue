*************************************************
How to set-up the nightscout-phillips integration
*************************************************

| This project is made to display the insulin level of a pump controlled via nighscout. Adjusting the light of the room depending on what you set your environment variables.

Setting up
==========
Setting this up shouldn't be hard. There are 2 ways to do this, either editing the `docker-compose.yml <https://github.com/Felaxus/nightscout_hue/blob/main/docker-compose.yml>`_ file (preferred)
or you can edit the config.py file. Environment values (`docker-compose.yml <https://github.com/Felaxus/nightscout_hue/blob/main/docker-compose.yml>`_) have preference over config.py.

Using docker-compose
^^^^^^^^^^^^^^^^^^^^
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