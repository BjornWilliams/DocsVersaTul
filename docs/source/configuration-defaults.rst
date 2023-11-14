Configuration Defaults
===============================

Getting Started
----------------
The VersaTul Configuration default project enables the ability to quickly setup default settings for VersaTul
projects. Currently supported projects are:

- Caching - *VersaTul.Configuration.Defaults.Caching*
- Entity Framework Core - *VersaTul.Configuration.Defaults.EntityFrameworkCore*
- Mailer - *VersaTul.Configuration.Defaults.Mailer*
- MongoDb - *VersaTul.Configuration.Defaults.MongoDB*
- Sql - *VersaTul.Configuration.Defaults.Sql*
- MsSql - *VersaTul.Configuration.Defaults.MsSql*
- Logger - *VersaTul.Configuration.Defaults.Logger*

Installation
------------

To use VersaTul Configuration Defaults, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Configuration.Defaults -Version latest

Main Components
----------------
#. ``ConfigurationBuilder`` : Provides the functionality needed to setup default settings. All builder classes are derived from this class.
#. ``Builder`` : Project specific builders. These can be found under their respective namespaces.

Functional Summary
------------------
#. **ConfigurationBuilder ConfigurationBuilder.AddOrReplace()** : Overloaded method for adding or replacing the value at the given key in the configuration dictionary.
#. **ConfigSettings ConfigurationBuilder.BuildConfig()** : Create a new ConfigSettings dictionary from the underlining dictionary keys and values added during setup.

Code Examples
--------------

.. code-block:: c#
    :caption: Configuration builder MongoDb example.

    using VersaTul.Configuration.Defaults.MongoDB;

    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            //Default configs with connection name replacement.
            var configSettings = new Builder()
                .AddOrReplace("MongoDb", "mongodb://root:password123@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/DemoDB?replicaSet=replicaset")
                .BuildConfig();
            
            // Registering the settings so that it can be used to build DataConfiguration<>.
            builder.RegisterInstance(configSettings);

            //Singletons
            builder.RegisterGeneric(typeof(DataConfiguration<>)).As(typeof(IDataConfiguration<>)).SingleInstance();            
        }
    }

Project Config Settings
------------------------

.. _tbl-grid:

+--------------+-----------------------+------------------+
| Project Name | Setting Name          | Default Value    |
+==============+=======================+==================+
| Caching      | CacheDuration         | 60s              |
+--------------+-----------------------+------------------+
| efCore       | EfDbConnectionName    | DBCon            |
+--------------+-----------------------+------------------+
| Mailer       | SmtpServer            | 127.0.0.1        |
+--------------+-----------------------+------------------+
| Mailer       | SmtpPort              | 25               |
+--------------+-----------------------+------------------+
| Mailer       | SmtpUserName          | User-Defined     |
+--------------+-----------------------+------------------+
| Mailer       | SmtpPassword          | User-Defined     |
+--------------+-----------------------+------------------+
| Mailer       | FromAddress           | User-Defined     |
+--------------+-----------------------+------------------+
| Mailer       | ToAddress             | User-Defined     |
+--------------+-----------------------+------------------+
| Mailer       | MaxAttachmentSize     | 10000000 Bytes   |
+--------------+-----------------------+------------------+
| MongoDB      | MongoDbConnectionName | MongoDb          |
+--------------+-----------------------+------------------+
| MongoDB      | SocketTimeout         | 600000ms         |
+--------------+-----------------------+------------------+
| MongoDB      | ConnectTimeout        | 600000ms         |
+--------------+-----------------------+------------------+
| MongoDB      | WorkingDatabaseName   | User-Defined     |
+--------------+-----------------------+------------------+
| MongoDB      | MaxConnectionIdleTime | 600000ms         |
+--------------+-----------------------+------------------+
| MongoDB      | EnabledSslProtocols   | false            |
+--------------+-----------------------+------------------+
| MsSql        | BulkCopyTimeout       | 1800s            |
+--------------+-----------------------+------------------+
| Sql          | CommandTimeout        | 600s             |
+--------------+-----------------------+------------------+
| Sql          | SqlDbConnectionName   | DBCon            |
+--------------+-----------------------+------------------+
| Logger.File  | MaxFileSize           | 2000000000 Bytes |
+--------------+-----------------------+------------------+
| Logger.File  | LogFileName           | log              |
+--------------+-----------------------+------------------+
| Logger.File  | FilePath              | User-Defined     |
+--------------+-----------------------+------------------+
| Logger.Web   | BaseUrl               | User-Defined     |
+--------------+-----------------------+------------------+
| Logger.Web   | LogEndPoint           | User-Defined     |
+--------------+-----------------------+------------------+
