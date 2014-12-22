program repeatUntilLoop;
var a: integer;
begin
   a := 10;
   repeat
      writeln(a);
      a := a + 1;
   until a = 14;
end.