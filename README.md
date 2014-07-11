CERN-ImageFactory-Client
========================

The Client script to talk to ImageFactory's REST API.
[ImageFactory](github.com/redhat-imaging/imagefactory) is a tool to automate build and upload of Guest VM Images and is being deployed on CERN OpenStack Cloud

##Features##
*   Print ImageFactory version and API version info
*   Create and Upload an image to a Cloud
    * Current guest OS support: Fedora 7-19, RHEL 5.x and 6.x
    * Current cloud support: OpenStack


##Using ImageFactory-Client##
Building an image begins with a template describing what to build. See an example
of such a template below. See the [schema documentation for TDL](http://imgfac.org/documentation/tdl/TDL.html)
for more detail on creating a template. Note that a template is **not** tied to
a specific cloud.

    <template>
        <name>f12jeos</name>
        <os>
            <name>Fedora</name>
            <version>12</version>
            <arch>x86_64</arch>
            <install type='iso'>
                <iso>http://download.fedoraproject.org/pub/fedora/linux/releases/12/Fedora/x86_64/os/</iso>
            </install>
        </os>
    </template>


Next, use the ImageFactory_Client command with the following parameters -

* Provider definition file
* Your openrc credentials file
* The template to be used for building an image.
* *Optional:* The template's KickStart file

Example -
```
$ ./ImageFactory_Client ~/provider_definition ~/openrc.sh ~/slc6-server-x86_64.tdl ~/slc6-server-x86_64.ks
```

That's it!  You can now launch an instance of this image using the cloud
provider's management console.
