using VersaTul.Data.Contracts;

var request = new PagedRequest { PageNumber = 3, PageSize = 20 };
Console.WriteLine($"Skip {request.Skip} rows; take {request.PageSize}.");
