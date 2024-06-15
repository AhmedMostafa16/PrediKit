<div align="center" style="display: flex; flex-direction: row; justify-content: center; align-items: center;">

<img src="docs/assets/images/predikit_face.jpg" alt="PrediKit" width="550" height="350" style="margin-right: 0px;">
<img src="docs/assets/images/visualization.jpg" alt="PrediKit2" width="550" height="350" style="margin-left: 0px;">

</div>

<div align="center">

# PrediKit

[𝙹𝚘𝚒𝚗 𝙳𝚒𝚜𝚌𝚘𝚛𝚍]() ✦ [𝚆𝚎𝚋𝚜𝚒𝚝𝚎]() ✦ [𝙳𝚎𝚖𝚘]() ✦ [𝙷𝚘𝚠 𝚝𝚘 𝙸𝚗𝚜𝚝𝚊𝚕𝚕 ](#how-to-install) ✦ [𝙲𝚘𝚗𝚝𝚛𝚒𝚋𝚞𝚝𝚎](#join-us-contribute)

---

</div>

### PrediKit is a scalable, cloud-based data science and machine learning platform that enables users across different expertise levels to harness the power of data through an easy-to-use visual interface. PrediKit provides end-to-end capabilities for building data workflows, performing analytics, and deploying machine learning models without requiring coding.

<br>

<div align="center">

## How does it work?

</div>

PrediKit platform takes you dataset to enable you prepare the data and build a Machine Learning model that performs a
purpose based on your dataset along with your preferences

The process is as follows:

1. **Data Ingestion**:

2. **Data Preparation**:

3. **Model Training**:

4. **Model Deployment**:
<br/>
<div align="center">

## How to install

</div>

Follow these steps to set up the environment and run the application.

1. Fork the repository [here](https://github.com/AhmedMostafa16/PrediKit/fork).

2. Clone the forked repository.

   ```bash
   git clone https://github.com/<YOUR-USERNAME>/PrediKit.git
   cd PrediKit
   ```

3. Create a Python Virtual Environment:

   - Using [pyenv.sh](/pyenv.sh) script to automate setting up virtual environment and installing dependencies

   ```bash
   ./pyenv.sh
   ```

   - Using [virtualenv](https://learnpython.com/blog/how-to-use-virtualenv-python/):

     _Note_: Check how to install virtualenv on your system here [link](https://learnpython.com/blog/how-to-use-virtualenv-python/).

     ```bash
     virtualenv env
     ```

   **OR**

   - Create a Python Virtual Environment:

     ```bash
     python -m venv env
     ```

4. Activate the Virtual Environment.

   - On Windows.

     ```bash
     env\Scripts\activate
     ```

   - On macOS and Linux.

     ```bash
     source env/bin/activate
     ```

     **OPTIONAL (For pyenv users)**

   Run the application with pyenv (Refer this [article](https://realpython.com/intro-to-pyenv/#installing-pyenv))

   - pyenv installer
     ```
        curl https://pyenv.run | bash
     ```
   - Install desired python version

     ```
       pyenv install -v 3.12.0
     ```

   - pyenv with virtual enviroment

     ```
        pyenv virtualenv 3.12.0 venv
     ```

   - Activate virtualenv with pyenv
     ```
        pyenv activate venv
     ```

5. Install Dependencies:

- Manually

```bash
pip install -r requirements.txt
```

- or just use the install.sh script

```bash
./install.sh
```

## Join Us, Contribute!

</div>

Pull Requests & Issues are not just welcomed, they're celebrated! Let's create together.

<!-- 🎉 Join our lively [Discord]() community and discuss away! -->

💡 Spot a problem? Create an issue!

👩‍💻 Dive in and help resolve existing [issues](https://github.com/AhmedMostafa16/PrediKit/issues).

🔔 Share your thoughts in our [Discussions & Announcements](https://github.com/AhmedMostafa16/PrediKit/discussions).

🚀 Explore and improve our [Landing Page](). PRs always welcome!

📚 Contribute to the [PrediKit Docs]() and help people get started with using the software.

#### Tech Stack

Current:

- Python webapp in FastAPI.

![Python](./docs/assets/icons/python-banner.svg)

In Development:

- Check the [webapp](/frontend/web/) folder for a Next JS app in development. (In Development)

![Python](./docs/assets/icons/python-banner-yellow.svg) ![Tailwind CSS](./docs/assets/icons/tailwind-banner.svg)![FastAPI](./docs/assets/icons/fastapi-banner.svg) ![Next JS](/docs/assets/icons/next-js.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi) ![TypeScript](./docs/assets/icons/typescript-banner.svg) ![HTML5](./docs/assets/icons/html5-banner.svg) ![CSS3](./docs/assets/icons/css3-banner.svg) ![& More](./docs/assets/icons/more-banner.svg)

<br/>

<div align="center">

---

<!--
### Our Contributors ✨

<a href="https://github.com/mghalix/Banque-Misr/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=mghalix/Banque-Misr" />
</a> -->
