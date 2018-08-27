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

The Walkthrough XBlock uses a simple XML-based structure as shown below:
```bash
<walkthrough schema_version='1'>
    <step>
        <name>
            #navmaker
        </name>
        <find>
        </find>
        <dataStep>
            1
        </dataStep>
        <dataIntro>
            Welcome to the platform walkthrough tour! Let's start by
            exploring the tabs at the top of the page.
        </dataIntro>
        <dataPosition>
             right
        </dataPosition>
    </step>
</walkthrough>
```
To add a new step, first add the opening and closing tags, <step> and </step>. 
Inside, the tags `<name>`, `<dataStep>`, `<dataIntro>`, and `<dataPosition>` must be defined, with the option of defining `<find>`. 

`<name>`: the name of the html element, found by inspecting the page. 
`<find>`: further specification on the element to be highlighted (when found inside another element).
`<dataStep>`: the step number in the walkthrough process.
`<dataIntro>`: the text that will appear to explain the element.
`<dataPosition>`: where relative to the element the text will appear (top, bottom, right, left).
