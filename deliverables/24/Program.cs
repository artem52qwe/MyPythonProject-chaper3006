using System;
using System.Globalization;

public sealed class Analysis
{
    public long Sum { get; private set; }
    public decimal Average { get; private set; }
    public int Minimum { get; private set; }
    public int Maximum { get; private set; }

    public Analysis(long sum, decimal average, int minimum, int maximum)
    {
        Sum = sum;
        Average = average;
        Minimum = minimum;
        Maximum = maximum;
    }
}

public static class Program
{
    public static Analysis AnalyzeNumbers(int[] numbers)
    {
        if (numbers == null) throw new ArgumentNullException("numbers");
        if (numbers.Length == 0)
            throw new ArgumentException("At least one integer is required.");

        // A long accumulator safely holds the sum of an int-indexed int array.
        long sum = 0;
        int minimum = numbers[0];
        int maximum = numbers[0];
        foreach (int value in numbers)
        {
            sum += value;
            if (value < minimum) minimum = value;
            if (value > maximum) maximum = value;
        }
        return new Analysis(sum, (decimal)sum / numbers.Length, minimum, maximum);
    }

    public static int Main()
    {
        Console.WriteLine("Enter integers separated by spaces:");
        string input = Console.ReadLine();
        if (String.IsNullOrWhiteSpace(input))
        {
            Console.WriteLine("Error: empty input.");
            return 1;
        }
        string[] tokens = input.Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
        int[] numbers = new int[tokens.Length];
        for (int index = 0; index < tokens.Length; index++)
        {
            if (!Int32.TryParse(tokens[index], NumberStyles.Integer,
                                CultureInfo.InvariantCulture, out numbers[index]))
            {
                Console.WriteLine("Error: invalid Int32 value at position {0}.", index + 1);
                return 1;
            }
        }
        Analysis result = AnalyzeNumbers(numbers);
        Console.WriteLine("sum={0}; avg={1}; min={2}; max={3}", result.Sum,
                          result.Average.ToString(CultureInfo.InvariantCulture),
                          result.Minimum, result.Maximum);
        return 0;
    }
}
