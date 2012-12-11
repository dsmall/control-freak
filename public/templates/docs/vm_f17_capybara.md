Creating a VMware Fusion VM for Fedora 17 and installing Capybara
====================

--


### Baseline State
The target machine is an iMac with 8 GB RAM running OS X Lion.

    Mac OS X 10.7.5
    VMware Fusion Pro v5.0.2
 
### Creating the Fedora 17 VM
From Virtual Machine Library choose Add New...

1. Click Continue without disc
2. Click Choose a disc or disc image..., click again to choose a disk image, in this case
`Fedora-17-x86_64-netinst.iso`, then click Continue.
3. Set Operating System to Linux and Version to Fedora 64-bit, then click Continue.
4. Accept the default settings and click Finish, then set the name of the new VM.

Fusion boots the ISO

1. Tab to Troubleshooting and after `quiet` add `resolution=1024x768`. This makes
the Back and Next buttons visible.
2. Proceed with the installation, following the instructions.
3. When you get to the installation type screen, choose `Software Development` then click Next.
4. Wait for the installation to finish (an hour or so).

### Updating Fedora to allow VMware Tools compilation
This section and the hint about specifying the screen resolution is from the
[cat slave diary][csd] blog. When installation is complete, reboot Fedora, create a user
and log in. Open a terminal window and type the following commands:

    $ sudo yum update
    $ sudo reboot
    $ sudo yum install kernel-devel kernel-headers gcc make
    
If you followed the instructions above and in particular chose the `Software Development` option,
there should be nothing to install.

### Installing VMWare Tools
From the `Virtual Machine` menu choose `Install VMware Tools`. This mounts a virtual CD.
In the terminal window, type:

    $ tar zxf /run/media/`whoami`/VMware\ Tools/VMw*.tar.gz
    
You can use command completion to verify that the path is correct. If you cannot type
backquotes, replace `whoami` with your login name. To install the tools type:

    $ cd vmware-tools-distrib
    $ sudo ./vmware-install.pl

You can accept the default response (in square brackets) to all options by typing enter.

After installation is complete, reboot and log in. You should now be able to resize the VM window
and its contents will automatically resize or work in full screen.
You can also copy and paste between the OS X and Fedora environments.

### Installing Ruby Version Manager
Ruby Version Manager (RVM) allows you to easily install, manage and work with
multiple ruby environments, from rubies (interpreters) to sets of gems (packages).
The [RVM web page][rvm] is the primary resource.
Visit the [installation documentation][rvmid] and read the note about
__External tutorials__. We will follow the installation instructions exactly.
Open a terminal window and copy and execute the command to install RVM with ruby:

    $ \curl -L https://get.rvm.io | bash -s stable --ruby

After downloading some files, installation pauses to allow prerequisites to be
installed. In this case there were none. Type q to continue. No binary rubies are
availabile so yaml and ruby are downloaded and compiled, after which rubygems are
installed. Finally the following message appears:

* To start using RVM you need to run `source /Users/davids/.rvm/scripts/rvm`
in all your open shell windows, in rare cases you need to reopen all shell windows.

Copy this line and execute it. After this you should be able to use RVM and confirm that the
stable release version of the ruby interpreter has been installed:

    $ rvm version
    rvm 1.17.0 (stable) by Wayne E. Seguin <wayneeseguin@gmail.com>, Michal Papis <mpapis@gmail.com> [https://rvm.io/]
    $ rvm list
    rvm rubies
    =* ruby-1.9.3-p327 [ x86_64 ]

### Setting up a new Ruby Project
As its name implies, RVM allows you to install multiple versions of ruby and choose which to use. It
also allows you to isolate each of your projects. To create a new project, create a new directory, then
using your text editor, create an `.rvmrc` file. For example, assuming the project directory is
`capybara/`, you could create an `.rvmrc` file with the following content:

    rvm 1.9.3-p327@capybara

This line specifies that the project in this folder should use `ruby-1.9.3-p327`. The project's
gems will be installed in the Gemset `capybara`. The folder and Gemset names do not need to be the
same but it is convenient if they are. Having created and saved the `.rvmrc` file, change into the
project directory and you will be asked to confirm that you trust it:

    $ cd capybara
    ...
    Do you wish to trust this .rvmrc file? (/home/dsmall/capybara/.rvmrc)
    y[es], n[o], v[iew], c[ancel]> y
    Gemset 'capybara' does not exist, 'rvm gemset create capybara' first, or append '--create'.

Note the message after you type `y`. Copy the command and execute it:

    $ rvm gemset create capybara
    gemset created capybara	=> /home/dsmall/.rvm/gems/ruby-1.9.3-p327@capybara

Having done this, `cd` out of the project directory and back into it and confirm there are no messages.

### Using your new Ruby Project
Once you have set up a project directory with an `.rvmrc` file, RVM will intercept gem commands and
redirect their output to the project gems directory shown above. For example, `cd` into the new project
directory and install the capybara gem and its dependencies:

    $ gem install capybara
    Fetching: ...
    Building native extensions.  This could take a while...
    ...
    13 gems installed
    $ gem list
    *** LOCAL GEMS ***

    bundler (1.2.2)
    capybara (2.0.1)
    childprocess (0.3.6)
    ffi (1.2.0)
    libwebsocket (0.1.6.1)
    mime-types (1.19)
    multi_json (1.3.7)
    nokogiri (1.5.5)
    rack (1.4.1)
    rack-test (0.6.2)
    rake (10.0.2)
    rubygems-bundler (1.1.0)
    rubyzip (0.9.9)
    rvm (1.11.3.5)
    selenium-webdriver (2.26.0)
    websocket (1.0.4)
    xpath (1.0.0)
    
If you now `cd` up a level out of the project directory, `capybara` will no longer be listed:

    $ cd ..
    $ gem list
    *** LOCAL GEMS ***

    bundler (1.2.2)
    rake (10.0.2)
    rubygems-bundler (1.1.0)
    rvm (1.11.3.5)

The gem `capybara` and its dependencies will only be available in the `capybara/` project directory and below it.

### Using a Macintosh keyboard
You can set up Fedora to work well with a Macintosh keyboard. These instructions are for the Apple
Wireless Keyboard (UK model with £ sign at Shift-3):

1. In your Fedora user menu (at the right of the menu bar), choose System Settings.
2. Click the Keyboard icon
3. Click Layout Settings
4. Click + to add a new keyboard
5. Click English (UK, Macintosh)
6. Click Preview to check that the layout matches your keyboard
7. Click Add
8. Select the default keyboard and click - to delete it
9. Click the Options... button
10. Expand Key to choose 3rd level
11. Tick Any Alt key

Check that all the keys you need for programming are working correctly. In this particular case, we need `Alt-3` to type `#`.

### Installing the Chrome browser
With the above installation, you can execute a Capybara script for `:selenium` and it will use the Firefox browser which is installed with
Fedora. To install Chrome and use it with Selenium Webdriver 2.0:

1. Go to the Chrome download page, choose `64 bit .rpm for Fedora` and click `Accept and Install`
2. After Chrome and its dependencies have been downloaded and installed, open Chrome to check that it's working
3. Go to [code.google.com/p/chromedriver/][cgc]  and download `ChromeDriver server for linux64`
4. In your Downloads folder extract the `chromedriver` executable
5. Move or copy `chromedriver` to directory in your PATH, for example `cp chromedriver /home/dsmall/.rvm/bin/`
6. Modify your Capybara script to use the`:chrome` driver and test

<small>Updated 28 Nov 2012</small>

[csd]: http://www.greebo.net/2012/06/01/fedora-17-install-on-vmware-fusion-4-workstation-8/
[rvm]: https://rvm.io/
[rvmid]: https://rvm.io/rvm/install/
[cgc]: http://code.google.com/p/chromedriver/downloads/list