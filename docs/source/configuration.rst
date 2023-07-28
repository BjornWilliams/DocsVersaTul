Configuration
======================

Getting Started
----------------
The VersaTul Configuration project enables the ability to get the values of the specified keys stored in the settings dictionary.
Much like the DOTNET ``IConfiguration`` interface this configuration project provides a way to cleanly pass settings into an application.
The VersaTul projects that needs settings are built on top of Configuration. However this project can be extended to be used in other custom projects as well.

Installation
------------

To use VersaTul Configuration, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Configuration -Version latest


Main Components
----------------
#. ``IConfiguration`` : Represents a configuration file that is applicable to a particular application, or resource.
#. ``IAppConfiguration`` : Represents the base application configuration.
#. ``Configuration`` : Abstract class implementing ``IConfiguration``. This class must be inherited.
#. ``AppConfiguration`` : Abstract class implementing ``IAppConfiguration``. This class must be inherited.
#. ``ConfigSettings`` : Represents a collection of Key Values. Keys are strings and Values are object.

Functional Summary
------------------
#. **T IConfiguration.Get<T>(string name = null)** : Gets the value of the specified key stored in the settings dictionary. *Note:* If no name is supplied the calling property name is used for the setting lookup. 
#. **T IConfiguration.GetOrDefault<T>(string name = null)** : Get the value of the specified key stored in the settings dictionary. However, if the key is not present then the default of the type T is returned.


Code Examples
-------------

.. code-block:: c#
    :caption: Configuration inherited
    :emphasize-lines: 64, 67

    // Inherits the Configuration base class and extends its functionality with 
    // the additional properties.
    public class BaseConfig : Configuration
    {
        public BaseConfig(ConfigSettings configSettings) : base(configSettings) { }

        public int Property1 => Get<int>(); //uses the property name as setting key.

        public string FilePath => Get<string>("FileSourcePath");

        public string Property3 => Get<string>();
    }

    // configuration settings - This can be from any source e.g app.setting.json, 
    // app.config ...
    var configSettings = new ConfigSettings
    {
        { "Property1", 100 },
        { "FileSourcePath", "This is File Source Path" },
        { "Property3", "This is property 3" }
    };

    //initializing configuration class
    var baseConfig = new BaseConfig(configSettings);

    //pulling value from config using property.
    var result = baseConfig.Property1;