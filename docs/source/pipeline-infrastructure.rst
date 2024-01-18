Pipeline Infrastructure
================================

Getting Started
----------------
The VersaTul Pipeline Infrastructure project is designed to provide a very useful and neat pattern in the scenario when a set of filtering/processing needs to be performed on an object to transform it into a useful state. 
The project is the complete implementation of Pipeline pattern in a generic fashion.

Installation
------------

To use VersaTul Pipeline Infrastructure, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Pipeline.Infrastructure -Version latest


Main Components
----------------
#. ``IStep<TIn, TOut>`` : A step represents the work to be done on a given input with the given return type.
#. ``Pipeline<TIn, TOut> : IStep<TIn, TOut>`` : Represents an accumulative set of steps that can be performed on a given input.
#. ``PipelineExtensions`` : Provides an easy way of extending objects with pipeline steps.

Functional Summary
------------------
#. **TOut ISteps<TIn, TOut>.Execute(TIn input);** : Steps implementing this method would perform processing on the input type{TIn}.
#. **Func<TIn, TOut> Pipeline<TIn, TOut>.Step** : Property on the Pipeline that gets the starting step associated with this pipeline.
#. **TOut PipelineExtensions.AddStep<TIn, TOut>(this TIn input, IStep<T, U> step)** : An extension method for Providing an easy way of extending objects with pipeline steps.

Code Examples
-------------
.. code-block:: c#
    :caption: Simple Example of Pipeline Step Setup

    // Pipeline step to add a number to input.
    public class AddOneStep : IStep<int, int>
    {
        public int Execute(int input)
        {
            return input + 1;
        }
    }

    // Pipeline step to convert the input.
    public class IntToStringStep : IStep<int, string>
    {
        public string Execute(int input)
        {
            return input.ToString();
        }
    }

    // Pipeline step that is optional.
    public class OptionalStep<TIn, TOut> : IStep<TIn, TOut> where TIn : TOut
    {
        private readonly IStep<TIn, TOut> Step;
        private readonly Func<TIn, bool> choice;

        // passing the optional function during construction for later use.
        public OptionalStep(Func<TIn, bool> choice, IStep<TIn, TOut> Step)
        {
            this.choice = choice;
            this.Step = Step;
        }

        public TOut Execute(TIn input)
        {
            // runing optional check during pipeline processing.
            if (!choice(input))
            {
                return input;
            }

            return Step.Execute(input);
        }
    }

.. code-block:: c#
    :caption: Simple Example of Pipeline Usage

    // Using nested pipeline to work with different types.

    // Example pipeline with steps setup.
    public class CompoundPipeline : Pipeline<int, string>
    {
        public CompoundPipeline()
        {
            Step = input => input
                .AddStep(new AnInitialStep())
                .AddStep(new InnerPipeline()) //InnerPipeline used by CompoundPipeline
                .AddStep(new IntToStringStep())
                .AddStep(new DoSomethingWithAStringStep());
        }
    }

    // A Pipeline that's called by another pipeline.
    public class InnerPipeline : Pipeline<string, int>
    {
        public InnerPipeline()
        {
            Step = input => input
            .AddStep(new DoSomethingWithAnIntegerStep())
            .AddStep(new SomethingElseWithAnIntegerStep())
            .AddStep(new OptionalStep<int, int>(i => i > 5, new AddOneStep()));
        }
    }


.. code-block:: c#
    :caption: Simple Example of using Pipeline to Format Input

    // interface for formatters.
    public interface IFormatter : IStep<PropertyData, PropertyData> { }

    // Input model 
    public class PropertyData
    {
        // See the display attribute project for more details. 
        public DisplayAttribute Attribute { get; set; }

        public object Value { get; set; }        
    }

    // Date formatter - use to format an inputted value to a date string value.
    public class DateFormatter : IFormatter
    {
        public PropertyData Execute(PropertyData input)
        {
            if (input == null) { return input; }

            if (input.Value == null) { return input; }

            if (string.IsNullOrEmpty(input.Attribute.DateFormattingString)) { return input; }

            var type = input.Value.GetType();

            if (type != typeof(DateTime)) { return input; }

            input.Value = ((DateTime)input.Value).ToString(input.Attribute.DateFormattingString);

            return input;
        }
    }

    // Decimal formatter - use to format an inputted value to a rounded decimal value.
    public class DecimalFormatter : IFormatter
    {
        public PropertyData Execute(PropertyData input)
        {
            if (input == null) { return input; }

            if (input.Value == null) { return input; }

            if (input.Attribute.Decimals == int.MinValue || input.Attribute.Decimals == int.MaxValue) { return input; }

            var type = input.Value.GetType();

            if (type != typeof(decimal) && type != typeof(double) && type != typeof(float)) { return input; }

            input.Value = decimal.Round((decimal)input.Value, input.Attribute.Decimals);

            return input;
        }
    }

    // Format Pipeline used to perform formatting on inputted values.
    public class FormatPipeline : Pipeline<PropertyData, PropertyData>
    {
        public FormatPipeline()
        {
            Step = input => input
                .AddStep(new DateFormatter())
                .AddStep(new DecimalFormatter());
        }
    }

    // Usage could look something like the following:
    public class DisplayAnalyzer
    {
        // store pipeline instance
        private readonly FormatPipeline formatPipeline;
       
        public DisplayAnalyzer()
        {
            // setup the pipeline for use
            formatPipeline = new FormatPipeline();
        }
       
        public object FormatValue(DisplayAttribute displayAttribute, object propertyValue)
        {
            if (displayAttribute == null) { return propertyValue; }

            // using the pipeline to format the given value.
            // value PropertyData will be passed through all steps and properly formatted 
            // by valid steps.
            propertyValue = formatPipeline.Execute(new PropertyData
            {
                Attribute = displayAttribute,
                Value = propertyValue
            })
            .Value;

            return propertyValue;
        }
    }



Changelog
-------------

V1.0.7

* Added Async support

V1.0.6

* Minor fixes
* xml comments code

V1.0.5

* Code ported to dotnet core
* Documentaion completed
    
