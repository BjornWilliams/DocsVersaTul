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

Installation
------------

To use VersaTul Configuration Defaults, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Configuration.Defaults -Version latest

Main Components
----------------
1. ``ConfigurationBuilder`` : Provides the functionality needed to setup default settings. All builder classes are derived from this class.
2. ``Builder`` : Project specific builders. These can be found under their respective namespaces.

Functional Summary
------------------
1. **AddOrReplace(string key, object value)** : Used to add or replace the given key and value in the configuration dictionary. For the given key/value options.
2. **AddOrReplace(IEnumerable<KeyValuePair<string, object>> valuePairs)** : Used to add or replace a list of keys and values in the configuration dictionary.
3. **AddOrReplace(IDictionary<string,object> keyValuePairs)** : Used to add or replace a list of keys and values in the configuration dictionary.

Code Examples
--------------

.. code-block:: c#
    :caption: Configuration builder MongoDb example.

    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            //Default configs with connection name replacement.
            var configSettings = new MongoDB.Builder()
                .AddOrReplace("MongoDb", "mongodb://root:password123@sharedvm.local.com:27017,sharedvm.local.com:27018,sharedvm.local.com:27019/DemoDB?replicaSet=replicaset")
                .BuildConfig();
            
            builder.RegisterInstance(configSettings);

            //Singletons
            builder.RegisterGeneric(typeof(DataConfiguration<>)).As(typeof(IDataConfiguration<>)).SingleInstance();            
        }
    }

Default settings
----------------

.. _tbl-grid:

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | Cells may span columns.          |
+------------------------+------------+---------------------+
| body row 3             | Cells may  | - Table cells       |
+------------------------+ span rows. | - contain           |
| body row 4             |            | - body elements.    |
+------------------------+------------+---------------------+

Simple
-------

=====  =====  ======
   Inputs     Output
------------  ------
  A      B    A or B
=====  =====  ======
False  False  False
True   False  True
False  True   True
True   True   True
=====  =====  ======

+------------------+---------------+---------------+
| Project Name     | Setting Name   | Default Value |
+======================+============+===============+
| Defaults.Caching | CacheDuration  | 60            |
+----------------------+------------+---------------+
| Defaults.efCore  | ConnectionName | DBCon         |
+----------------------+------------+---------------+
| Defaults.Mailer  | SmtpServer     | 127.0.0.1     |
+----------------------+------------+---------------+
| Defaults.efCore  | SmtpPort       | DBCon         |
+----------------------+------------+---------------+
| Defaults.efCore  | SmtpUserName   | DBCon         |
+----------------------+------------+---------------+
| Defaults.efCore  | SmtpPassword   | DBCon         |
+----------------------+------------+---------------+
| Defaults.efCore  | MaxAttachmentSize | DBCon      |
+----------------------+------------+---------------+
