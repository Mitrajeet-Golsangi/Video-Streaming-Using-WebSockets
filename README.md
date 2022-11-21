# Live Video Streaming Application in Flutter using WebSockets <!-- omit in toc -->

# Contents <!-- omit in toc -->

- [1. Detailed Explanation](#1-detailed-explanation)
- [2. Setup Instructions](#2-setup-instructions)
  - [2.1. Network setup](#21-network-setup)
  - [2.2. Server Setup](#22-server-setup)
  - [2.3. Flutter Setup](#23-flutter-setup)

# 1. Detailed Explanation

- If you are interested in what is going on here you can check out my [medium post](https://medium.com/dscvitpune/creating-a-live-video-streaming-application-in-flutter-43e261e3a5cc) on this topic

# 2. Setup Instructions

## 2.1. Network setup

Assuming that this project will be run on a virtual device like emulator, you need to provide the ipv4 address for your network. This is required because the virtual device cannot detect the localhost (127.0.0.1) and will not be able to establish a connection using it.

1. Change the network ip in `/server/server.py` file on line 37
2. Change the websocket URL in the `/app/lib/constants/constants.dart` file in line 2

## 2.2. Server Setup

- Install `pipenv` package to get all the required packages
- Run the command below in the root directory

```
pipenv install
```

- Now you can activate the virtual environment using

```
pipenv shell;

```

- Start the server using the command in root directory

```
python ./server/server.py
```

## 2.3. Flutter Setup

- If you do not have the Flutter SDK you can get it [here](https://docs.flutter.dev/get-started/install?gclid=Cj0KCQiAveebBhD_ARIsAFaAvrEW2C-j9QMv4nmq9f-7DPnYFzanYvJUhXPT1rcTpjlb1gXwuv9oNvIaAmOoEALw_wcB&gclsrc=aw.ds) and you can follow the setup instruction from the docs
- Then you can run the command below to get all the required packages in the app directory

```
pub get
```

- Now run `flutter run` to start you project in the app directory
