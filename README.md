# Context-Aware IoT System

This project intends to pave the way towards context-awareness for IoT systems. In the scope of our work, context is understood as the connectivity characteristics of a device in a given environment. The documentation is available in the related  [github pages](https://nseydoux.github.io/ContextAwareIoTSystem/).

## Project Overview

<p align="center"><img src="https://github.com/DamarisMenfer/ContextAwareIoTSystem/blob/master/docs/Smartphone.png" width="400"></p>

The main idea of this project is to study a new way to locate users into the campus and secure access to data and applications by using devices connectivity as a context. The purpose of the project is to make an smart campus to improve experiences for students and staff. Using network analysis on how users move through the campus we can optimize services by the bias of an smartphone application.

When a device or a user is at a specific position, its connectivity can be used as a specific footprint. Using this information, whenever a device is in specific room of a smart campus, the connectivity footprint is extracted and compared to other footprint of campus devices. If the user footprint match with a footprint of a device within a room, we can offer access to specific services of the room by an application. Also, when two users devices share a similar footprint, they can gain the ability to exchange information.

For example, when someone enter the university restaurant with our application installed on the smartphone, he will get the menu of the day. Or, when someone is listening to a presentation in a room, he will receive the information about the presentation. As soon as the device leave the room, the access of the room information is lost but others informations are going to be displayed depending on the new footprint.

To do that, we need to develop an electronic device that will collect the connectivity footprints of a room to compare that to the footprint of an smartphone. After that, we are going to study if there exists a relationship between the GPS position and the footprint of the smartphone to validate our study. The technologies that we would like to test on this project are: Wifi, Bluetooth and LoRaWAN.
For the first part of the project, we need to design the hardware, collect the footprint data and perform the analytics. Then, we need to define and evaluate a metric allowing to compare two different footprints and then use this to compare the footprint of a device to the footprint of a user. If the metric is lower than a specific threshold, the user gains access to over the room information by the application that we are going to develop.

## Target audience

The aim of our project are the people who work and study on the campus. We want to simplify the live of these people inside the campus and also to make the university more attractive to new students.

## Expected Results

A live demonstration with a minimum viable product showing that you gain access to a device only if you are near this device, using all network information as connection information (including for example the Bluetooth and Wifi information from the smartphones in the room). We expect to have a hardware which is able to collect the connectivity footprints to compare that to the GPS coordinates of the smartphone to study the relationship between those data. Also, an application/interface for  the user to have access to the information provided by the hardware.
Also we will produce a report explaining the hardware, software, architecture and the evaluation of the correlation between GPS position and device footprint.
