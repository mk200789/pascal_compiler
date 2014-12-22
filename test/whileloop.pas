program whileLoop;
var a, b, c: integer;
begin
	a := 10;
	b := 12;
	c := 4;
	while  a < 12  do
	begin
		if ( a = 12) then
	  		writeln(a);
	  	else
	  		c := c + 1;
	  	a := a + 1;
	end;
end.