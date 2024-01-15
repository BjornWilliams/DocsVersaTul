EFCore
================

Getting Started
----------------
The VersaTul EFCore project provides the ability to quickly create project specific database repositories running on Microsoft Entity Framework Core ORM.
This project provides generic repository functionality that can be reused to create project specific repositories.
CRUD operations are defined both Synchronous and Asynchronous methods.

Installation
------------

To use VersaTul EFCore, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.EFCore -Version latest

Main Components
----------------
#. ``IUnitOfWork`` : Provides the functionality needed to support absolute unit of work.
#. ``BaseRepository<TEntity, TKey>`` : Abstract class that provides common functionality for CRUD operations.
#. ``BaseUnitOfWork`` : Default implementation of **IUnitOfWork**. 
#. ``DataConfiguration``` : Default implementation of the Configuration needed to connect to database.


Functional Summary
------------------
#. **TEntity BaseRepository<TEntity, TKey>.Add()** : Overloaded method for adding a given entity to the database.
#. **TEntity BaseRepository<TEntity, TKey>.AddRange()** : Overloaded method for adding a given list of entities to the database.
#. **TEntity BaseRepository<TEntity, TKey>.Find()** : Overloaded method for finding an entity with the given primary key values.
#. **IEnumerable<TEntity> BaseRepository<TEntity, TKey>.Get()** : Overloaded method for getting entities from the database.
#. **TEntity BaseRepository<TEntity, TKey>.Update()** : Overloaded method for updating a given entity in the database.
#. **TEntity BaseRepository<TEntity, TKey>.Remove()** : Overloaded method for deleting a given entity from the database.
#. **void BaseRepository<TEntity, TKey>.RemoveRange()** : Overloaded method for deleting a list of given entities from the database.

Code Examples
-------------
.. code-block:: c#
    :caption: Sample Repository Database Call

    //DataModel
    public class PlayerData
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public DateTime CreatedDate { get; set; }
    }

    //Create DbContext class which inherits from DbContext
    public class DatabaseContext : DbContext
    {
        // IDataConnection - provides the means by which the connection string
        // can be obtained from Configuration settings.
        private readonly IDataConnection dataConnection;
        
        public DatabaseContext(IDataConnection dataConnection)
        {
            this.dataConnection = dataConnection;
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                // using the GetConnectionString method to get the connection string at runtime.
                optionsBuilder.UseSqlServer(dataConnection.GetConnectionString());
            }
        }

        public DbSet<PlayerData> Players { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<PlayerData>().HasKey(x => x.Id);
        }
    }

    // Create a base repository interface that inherits IRepository<TEntity, TKey>
    // this will ensure all CRUD functionality is supported by every repository that inherits
    // from this interface. 
    // This technique is optional, am simply specifying the TKey value here as ``int`` so as to 
    // reduce complexity for project specific repositories.
    public interface IRepository<TEntity> : IRepository<TEntity, int> where TEntity : class, new()
    {

    }

    // Create project specific repository from IRepository<TEntity> interface.
    public interface IPlayerRepository : IRepository<PlayerData>
    {
        //project specific methods can be added here
    }

    // Create BaseRepository that inherits from BaseRepository<TEnity, TKey>
    // this will ensure all CRUD functionality is supported by every repository that inherits
    // from this base. Also specifying the TKey value as ``int`` to reduce complexity.
    // project specific DbContext should also be exposed from this class.
    public abstract class BaseRepository<TEnity> : BaseRepository<TEnity, int> where TEnity : class, new()
    {
        public BaseRepository(IUnitOfWork unitOfWork) : base(unitOfWork)
        {
            if(unitOfWork == null) throw new ArgumentNullException(nameof(unitOfWork));

            DbSet = unitOfWork.DataContext.Set<TEnity>();
        }

        protected DbSet<TEnity> DbSet { get; }

        protected DatabaseContext DatabaseContext => DataContext as DatabaseContext;   
    }

    // Create project specific UnitOfWork
    public class UnitOfWork : BaseUnitOfWork
    {
        public UnitOfWork(DatabaseContext dataContext) : base(dataContext) { }
    }

    // Create project specific repository
    public class PlayerRepository : BaseRepository<PlayerData>, IPlayerRepository
    {
        public PlayerRepository(IUnitOfWork unitOfWork) : base(unitOfWork) { }
    }

    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            //Configs
            var configSettings = new Builder()
                .AddOrReplace("DBCon", "Server=127.0.0.1;Database=DemoDb;User Id=sa;Password=password@123;Persist Security Info=True;")
                .BuildConfig();

            builder.RegisterInstance(configSettings);

            //Singletons
            builder.RegisterType<DataConfiguration>().As<IDataConnection>().SingleInstance();

            //Per Dependency
            builder.RegisterType<DatabaseContext>().AsSelf().InstancePerLifetimeScope();
            builder.RegisterType<UnitOfWork>().As<IUnitOfWork>().As<VersaTul.Data.EFCore.Contracts.IUnitOfWork>().InstancePerLifetimeScope();
            builder.RegisterType<PlayerRepository>().As<IPlayerRepository>().InstancePerLifetimeScope();
        }
    }

    // Repository usage could look like the following:
    [Route("api/players")]
    public class PlayerController: Controller
    {
        private readonly IPlayerRepository playerRepository;

        public PlayerController(IPlayerRepository playerRepository)
        {
            this.playerRepository = playerRepository;
        }

        // Get
        [HttpGet]
        public IActionResult GetPlayers()
        {
            var players = playerRepository.Get();

            return OK(players);
        }

        [HttpGet("{id}")]
        public IActionResult GetPlayer(int id)
        {
            var player = playerRepository.Get(id);

            if(player == null)
                return NotFound();

            return OK(player);
        }

        [HttpPost]
        public IActionResult CreatePlayer(CreatePlayerModel model)
        {
            var player = playerRepository.Add(new PlayerData {
                Name = model.Name,
                FirstName = model.FirstName,
                LastName = model.LastName
            });

            return OK(player);
        }

    }
    


Changelog
-------------