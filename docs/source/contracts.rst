Contracts
==================

Getting Started
----------------
The VersaTul Contracts project provides generic interfaces that are supported throughout the VersaTul ecosystem. 
Developers who may want to change the underline implementation of these contracts can create their own implementation of such contract 
and supply it to the VersaTul project in which they require to change the behavior. 

Installation
------------

To use VersaTul Contracts, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Contracts -Version latest

Main Components
----------------
#. ``IPredicate<T>`` : Represents an expression that can be applied to the type of T.

Functional Summary
------------------
#. **Expression<Func<T, bool>> IPredicate<T>.Condition** : Property to get or set an expression for filtering with Func of T.

Code Examples
-------------

.. code-block:: c#
    :caption: Example implementation as found in VersaTul.Data.MongoDB.Predicates.

    // Used to provide conditional expression to MongoDB engine. 
    public class WherePredicate<TEntity> : IPredicate<TEntity> where TEntity : IEntity
    {
        public WherePredicate(Expression<Func<TEntity, bool>> expression)
        {
            Condition = expression;
        }
        
        public Expression<Func<TEntity, bool>> Condition { get; set; }        
    }

    // sample use case 
    private void GetUsers(IUserRepository userRepository)
    {
        // used to provide filtering on UserName from the User model.
        var users = userRepository.Find(new WherePredicate<User>(model => model.UserName.Contains(SearchTerm)));

        if (users == null || !users.Any())
        {
            Print($"No user with the name {SearchTerm} was found.");
        }

        foreach (var user in users)
        {
            Print($"User {user.UserName} was found with Id:{user.Id}");
        }
    }
    


Changelog
-------------