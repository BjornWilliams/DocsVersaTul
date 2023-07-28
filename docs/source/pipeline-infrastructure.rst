Pipeline Infrastructure
================================

Getting Started
----------------
The VersaTul Pipeline Infrastructure project is designed to provide a very useful and neat pattern in the scenario when a set of filtering (processing) needs to be performed on an object to transform it into a useful state. 
The project is the complete implementation of Pipeline and Filter pattern in a generic fashion.

Installation
------------

To use VersaTul Caching, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Pipeline.Infrastructure -Version latest


Main Components
----------------
#. ``IFilter<T, U>`` : A filter represents the work to be done on a given input with the given return type.
#. ``Pipeline<T, U> : IFilter<T, U>`` : Represents an accumulative set of steps or filters that can be performed on a given input.
#. ``PipelineExtensions`` : Provides an easy way of extending objects with pipeline filters.

Functional Summary
------------------
#. **U IFilter<T, U>.Execute(T input);** : Filters implementing this method would perform processing on the input type{T}.
#. **Func<T, U> Pipeline<T, U>.Filter** : Property on the Pipeline that gets the filter associated with this pipeline.
#. **U PipelineExtensions.Filter<T, U>(this T input, IFilter<T, U> filter)** : An extension method for Providing an easy way of extending objects with pipeline filters.

Code Examples
-------------

.. code-block:: c#
    :caption: Simple Example of using Pipeline to Format Input

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
            Filter = input => input
                .Filter(new DateFormatter())
                .Filter(new DecimalFormatter());
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
            // value PropertyData will be passed through all filters and properly formatted 
            // by valid filters.
            propertyValue = formatPipeline.Filter(new PropertyData
            {
                Attribute = displayAttribute,
                Value = propertyValue
            })
            .Value;

            return propertyValue;
        }
    }

    
