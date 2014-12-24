program forLoop;
var a, b: integer;
begin
	b := 0;
	for a := 10  to 13 do
	begin
		b := b + a;
		writeln(a);
	end;
end.