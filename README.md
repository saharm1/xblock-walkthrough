Walkthrough
===========
This XBlock provides a walkthrough of the platform at the click of a button!

Installation
------------
To install the Walkthrough XBlock within your edX python environment, simply run this command:

```bash
$ pip install -r requirements.txt
```

Enabling in Studio
------------------
Go to `Settings -> Advanced Settings` and set `Advanced Module List` to `["walkthrough"]`.

Usage
------------------
Once the Walkthrough XBlock is enabled in Studio, you should see it a new Component button labeled `Advanced`:

Click the `Advanced` button and you should see the Walkthrough XBlock listed.

After you've selected the Walkthrough XBlock, a default set of steps will be inserted into your unit.

Customization
-------------
The button label, introduction, and steps can both be customized by clicking the `Edit` button on the component.

The steps of the walkthrough are respresented as a list of dictionaries. There
are 16 original steps that can be amended or removed.
