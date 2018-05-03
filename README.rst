===================
My personal website
===================

A website for me, with a blog and pages and image gallery and things as I need
them. Built on Wagtail.

Running
=======

Runs using ``docker-compose``:

.. code-block:: console

    $ docker-compose up

Publishing
==========

First, compile fresh frontend assets:

.. code-block:: console

    $ docker-compose build --no-cache --pull frontend
    $ docker-compose run --rm frontend npm run build

Build the image, tag it, then push:

.. code-block:: console

    $ docker-compose build --no-cache --pull backend
    $ docker tag timheap_backend timheap/timheap:latest
    $ docker push timheap/timheap:latest

Then pull the image down and restart which ever docker host it is deployed on.
