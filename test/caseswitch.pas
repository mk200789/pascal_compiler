program checkCase;
var grade: char;
begin
   grade := 'B';

   case ( grade) of
      'A' : writeln('Excellent!');
      'C', 'B' : writeln('Well done');
      'D' : writeln('You passed');
      'F' : writeln('Better try again');
   end;     
   writeln(grade);
end.