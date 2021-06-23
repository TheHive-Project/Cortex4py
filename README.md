<div>
  <p align="center">
    <a href="https://travis-ci.org/github/TheHive-Project/Cortex4py" target="_blank">
      <img src="https://travis-ci.org/TheHive-Project/Cortex4py.svg?branch=1.x" alt="Build status">
    </a>
    <a href="https://chat.thehive-project.org" target"_blank">
      <img src="https://img.shields.io/discord/779945042039144498" alt="Discord">
    </a>
    <a href="./LICENSE" target"_blank">
      <img src="https://img.shields.io/github/license/TheHive-Project/Cortex4py" alt="License">
    </a>
    <a href="https://pypi.org/project/cortex4py" target"_blank">
      <img src="https://img.shields.io/pypi/dm/cortex4py" alt="Pypi page">
    </a>
  </p>
</div>

# Cortex4py
Cortex4py is a Python API client for [Cortex](https://thehive-project.org/), a powerful observable analysis engine where observables such as IP and email addresses, URLs, domain names, files or hashes can be analyzed one by one using a Web interface.

Cortex4py allows analysts to automate these operations and submit observables in bulk mode through the Cortex REST API from alternative SIRP platforms, custom scripts or MISP.


# Features
Cortex4py 2 is compatible with Cortex 2 and does not work with Cortex 1. It can:
- Manage organizations
- Manage users
- Configure analyzers within an organization
- List and launch analyzers

For more details, please refer to the [full documentation](Usage.md).

**Note**: Cortex4py 2 requires Python 3. It does not support Python 2.

# Use It
On macOS and Linux, type:
```
sudo -H pip3 install cortex4py
```

or, if you already have it, update it:

```
sudo -H pip3 install -U cortex4py
```

If you are using Python on a Windows operating system, please forgo the `sudo` command.

# License
Cortex4py is an open source and free software released under the [AGPL](https://github.com/CERT-BDF/Cortex4py/blob/master/LICENSE) (Affero General Public License). We, TheHive Project, are committed to ensure that Cortex4py will remain a free and open source project on the long-run.

# Updates
Information, news and updates are regularly posted on [TheHive Project Twitter account](https://twitter.com/thehive_project) and on [the blog](https://blog.thehive-project.org/).

# Contributing
We welcome your contributions. Please feel free to fork the code, play with it, make some patches and send us pull requests using [issues](https://github.com/CERT-BDF/Cortex4py/issues).

We do have a [Code of conduct](code_of_conduct.md). Make sure to check it out before contributing.

# Support
Please [open an issue on GitHub](https://github.com/TheHive-Project/Cortex4py/issues/new) if you'd like to report a bug or request a feature. We are also available on [Discord](https://chat.thehive-project.org) to help you out.

If you need to contact the project team, send an email to <support@thehive-project.org>.

# Community Discussions
We have set up a Google forum at <https://groups.google.com/a/thehive-project.org/d/forum/users>. To request access, you need a Google account. You may create one [using a Gmail address](https://accounts.google.com/SignUp?hl=en) or [without one](https://accounts.google.com/SignUpWithoutGmail?hl=en).

# Website
<https://thehive-project.org/>
