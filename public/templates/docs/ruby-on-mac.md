Installing RVM on a Mac
====================

--

### Baseline State
The target machine is an iMac with 8 GB RAM running OS X Lion.
Xcode was downloaded from the Mac App Store in January 2012.

    Mac OS X 10.7.5
    Xcode 4.2.1 (build 4D502)
    ruby 1.8.7 (2012-02-08 patchlevel 358)
 
### Installing RVM
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
    rvm 1.16.20 (stable) by Wayne E. Seguin <wayneeseguin@gmail.com>, Michal Papis <mpapis@gmail.com> [https://rvm.io/]
    $ rvm list
    rvm rubies
    =* ruby-1.9.3-p327 [ x86_64 ]

### Setting up a new Ruby Project
As its name implies, RVM allows you to install multiple versions of ruby and choose which to use. It
also allows you to isolate each of your projects. To create a new project, create a new directory, then
using your text editor, create an `.rvmrc` file. For example, assuming the project directory is
`rascal-ruby`, you could create an `.rvmrc` file with the following content:

    rvm 1.9.3-p327@rascal-ruby

This line specifies that the project in this folder should use `ruby-1.9.3-p327`. The project's
gems will be installed in the Gemset `rascal-ruby`. The folder and Gemset names do not need to be the
same but it is convenient if they are. Having created and saved the `.rvmrc` file, change into the
project directory and you will be asked to confirm that you trust it:

    $ cd rascal-ruby
    ...
    Do you wish to trust this .rvmrc file? (/Users/davids/rascal-ruby/.rvmrc)
    y[es], n[o], v[iew], c[ancel]> y
    Gemset 'rascal-ruby' does not exist, 'rvm gemset create rascal-ruby' first, or append '--create'.

Note the message after you type `y`. Copy the command and execute it:

    $ rvm gemset create rascal-ruby
    gemset created rascal-ruby	=> /Users/davids/.rvm/gems/ruby-1.9.3-p327@rascal-ruby

Having done this, `cd` out of the project directory and back into it and confirm there are no messages.

### Using your new Ruby Project
Once you have set up a project directory with an `.rvmrc` file, RVM will intercept gem commands and
redirect their output to the project gems directory shown above. For example, `cd` into the new project
directory and install something:

    $ gem install selenium-webdriver
    Fetching: ...
    Building native extensions.  This could take a while...
    ...
    7 gems installed
    $ gem list
    *** LOCAL GEMS ***
    ...
    rvm (1.11.3.5)
    selenium-webdriver (2.26.0)
    
If you now `cd` up a level out of the project directory, `selenium-webdriver` will no longer be listed:

    $ cd ..
    $ gem list
    *** LOCAL GEMS ***
    ...
    rvm (1.11.3.5)

The gem `selenium-webdriver` will only be available in the `rascal-ruby` project.

<small>Updated 18 Nov 2012</small>

[rvm]: https://rvm.io/
[rvmid]: https://rvm.io/rvm/install/