Data MongoDB
================

Getting Started
----------------
The VersaTul Data MongoDB project provides functionality for working with Mongo Databases.
The project uses the repository design pattern to provide the functionality to Fetch, Add, Update, or Delete data.


Installation
------------

To use VersaTul Data MongoDB, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Data.MongoDB -Version latest

Main Components
----------------
#. ``IRepository<TEntity, TKey>`` : This is  a generic interface for supporting common CRUD operations.
#. ``IDataConfiguration<TKey>`` : This is a generic interface for fetching configuration settings. `TKey` represents the identity type of the collection.
#. ``IEntityMap<TEntity>`` : This is a generic interface that can be used to create BsonClassMaps for entities.
#. ``DataConfiguration<TKey>`` : This is the default implementation of the data configuration interface. 
#. ``BaseRepository<TEntity, TMap, TKey>`` : This is an abstract class providing common functionality for a MongoDB Database.
#. ``BaseMap<TEntity>`` : The default implementation of the `IEntityMap<IEntity>` interface. It provides general functionality that all inheriting custom project class maps can use when registering to the BsonClassMap.
#. ``WherePredicate<TEntity>`` : Thi is a helper class for generating search conditional expressions.
#. ``Entity`` : This is an abstract entity used for all Business Entities. It provides a default bson document Id property.

Functional Summary
------------------
#. **TEntity IRepository<TEntity, TKey>.Add(TEntity entity)** : Adds a single entity.
#. **void IRepository<TEntity, TKey>.Add(IEnumerable<TEntity> entities)** : Adds the list of entities to the collection.
#. **IEnumerable<TEntity> IRepository<TEntity, TKey>.Find(IPredicate<TEntity> predicate)** : Lazy loads any entity that matches given condition.
#. **TEntity IRepository<TEntity, TKey>.GetById(TKey id)** : Gets an entity for the given identifier.
#. **TEntity IRepository<TEntity, TKey>.Update(TEntity entity)** : Updates a single entity.
#. **void IRepository<TEntity, TKey>.Update(IEnumerable<TEntity> entities)** : Updates the given list of entities inside a collection.
#. **void IRepository<TEntity, TKey>.ChangeConnection()** : An overloaded method that can be used to change the underlining database connection of the active repository.
#. See :doc:`configuration-defaults` for more configuration settings.

Code Examples
-------------

.. code-block:: c#
    :caption: Sample Repository Database Call

    // DataModel inheriting the Entity class
    public class Car : Entity
    {
        public string Make { get; set; }
        public string Model { get; set; }
        public int Year { get; set; }
        public string EngineId { get; set; }
        public Owner Owner { get; set; }
        public IDictionary<string, object> ExtraElements { get; set; }
    }

    public class Owner
    {
        public string Name { get; set; }
        public int Age { get; set; }
        public HashSet<Size> ParkingSpots { get; set; }
        public IDictionary<string, object> ExtraElements { get; set; }

        public Owner()
        {
            ParkingSpots = new HashSet<Size>();
        }
    }

    // Mongo base class maps 
    // Also specifies the associated mongo collection 
    public class CarMap : BaseMap<Car>
    {
        public CarMap() : base("cars", model => model.ExtraElements) { }

        public override void Register(BsonClassMap<Car> classMap)
        {
            base.Register(classMap);
            classMap.GetMemberMap(model => model.EngineId).SetSerializer(new StringSerializer(BsonType.ObjectId));

            RegisterSub<Owner>((clsmp) =>
            {
                clsmp.GetMemberMap(model => model.ParkingSpots).SetSerializer(new SizeSerializer());
            }, 
            model => model.ExtraElements);
        }
    }

    // Project repository interface inheriting from IRepository<Entity>.
    public interface ICarRepository : IRepository<Car> { }


    // Project repository implementation, with BaseRepository inheritance.
    public class CarRepository : BaseRepository<Car, IEntityMap<Car>>, ICarRepository
    {
        public CarRepository(IDataConfiguration<string> configuration, IEntityMap<Car> entityMap) : base(configuration, entityMap)
        {
        }
    }

    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            //Configs
            var configSettings = new Builder()
                .AddOrReplace("MongoDb", "mongodb://root:password123@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/DemoDB?replicaSet=replicaset")
                .BuildConfig();

            builder.RegisterInstance(configSettings);

            //Singletons
            builder.RegisterGeneric(typeof(DataConfiguration<>)).As(typeof(IDataConfiguration<>)).SingleInstance();
            builder.RegisterType<CarRepository>().As<ICarRepository>().SingleInstance();
            builder.RegisterType<CarMap>().As<IEntityMap<Car>>().SingleInstance();

            //Per Dependency
        }
    }

    // Repository usage could look like the following:
    [Route("api/cars")]
    public class CarController: Controller
    {
        private readonly ICarRepository carRepository;

        public CarController(ICarRepository carRepository)
        {
            this.carRepository = carRepository;
        }

        // Get
        [HttpGet]
        public IActionResult GetCars()
        {
            var cars = carRepository.ToList();

            return OK(cars);
        }

        [HttpGet("{id}")]
        public IActionResult GetCar(string id)
        {
            var car = carRepository.GetById(id);

            if(car == null)
                return NotFound();

            return OK(car);
        }

         // find
        [HttpGet("find")]
        public IActionResult FindCars(string SearchTerm)
        {
            var cars = carRepository.Find(new WherePredicate<Car>(model => model.Make.Contains(SearchTerm) || model.Model.Contains(SearchTerm)));

            return OK(cars);
        }

        [HttpPost]
        public IActionResult CreateCar(CreateCarModel model)
        {
            var car = carRepository.Add(new Car {
                Make = model.Make,
                Model = model.Model,
                Year = model.Year
                EngineId = model.EngineId,
                Owner = new Owner { 
                    Name = model.Name,
                    Age = model.Age
                }
            });

            return OK(car);
        }

    }

.. code-block:: c#
    :caption: Changing database connection on the active repository to another configured database.

    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            //Configs
            var configSettings = new Builder()
                .AddOrReplace("MongoDb", "mongodb://root:password123@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/DemoDB?replicaSet=replicaset")
                .AddOrReplace("MongoCarsDb", "mongodb://root:password123@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/CarsDB?replicaSet=replicaset")
                .BuildConfig();

            builder.RegisterInstance(configSettings);

            //Singletons
            builder.RegisterGeneric(typeof(DataConfiguration<>)).As(typeof(IDataConfiguration<>)).SingleInstance();
            builder.RegisterType<CarRepository>().As<ICarRepository>().SingleInstance();
            builder.RegisterType<CarMap>().As<IEntityMap<Car>>().SingleInstance();

            //Per Dependency
        }
    }

    // Repository usage could look like the following:
    [Route("api/cars")]
    public class CarController: Controller
    {
        private readonly ICarRepository carRepository;

        public CarController(ICarRepository carRepository)
        {
            this.carRepository = carRepository;
        }

        // Get
        [HttpGet]
        public IActionResult GetCars()
        {
            // What if we wanted to pull the list of cars from another database.
            carRepository.ChangeConnection("MongoCarsDb")

            var cars = carRepository.ToList();

            return OK(cars);

            // Be mindful here in this example that because the car repository was stored as a SingleInstance
            // The next time its used it would still be using the MongoCarsDb connection. 
            // builder.RegisterType<CarRepository>().As<ICarRepository>().SingleInstance();
            // If this is not a desired behavior then ensure to dispose of the instance on every use 
            // or switch back the connection to default after use.
        }
    }

.. code-block:: c#
    :caption: Changing database connection on the active repository to another database using connection string.

    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            //Configs
            var configSettings = new Builder()
                .AddOrReplace("MongoDb", "mongodb://root:password123@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/DemoDB?replicaSet=replicaset")
                .BuildConfig();

            builder.RegisterInstance(configSettings);

            //Singletons
            builder.RegisterGeneric(typeof(DataConfiguration<>)).As(typeof(IDataConfiguration<>)).SingleInstance();
            builder.RegisterType<CarRepository>().As<ICarRepository>().SingleInstance();
            builder.RegisterType<CarMap>().As<IEntityMap<Car>>().SingleInstance();

            //Per Dependency
        }
    }

    // Repository usage could look like the following:
    [Route("api/cars")]
    public class CarController: Controller
    {
        private readonly ICarRepository carRepository;

        public CarController(ICarRepository carRepository)
        {
            this.carRepository = carRepository;
        }

        // Get
        [HttpGet]
        public IActionResult GetCars()
        {
            // What if we wanted to pull the list of cars from another database.
            // But we done know the connection string until runtime, this would be the ideal way to achieve this.
            carRepository.ChangeConnection(new MongoConnection("mongodb://root:password123@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/CarsDB?replicaSet=replicaset"))

            var cars = carRepository.ToList();

            return OK(cars);

            // Be mindful here in this example that because the car repository was stored as a SingleInstance
            // The next time its used it would still be using the MongoCarsDb connection. 
            // builder.RegisterType<CarRepository>().As<ICarRepository>().SingleInstance();
            // If this is not a desired behavior then ensure to dispose of the instance on every use 
            // or switch back the connection to default after use.
        }
    }


Changelog
-------------