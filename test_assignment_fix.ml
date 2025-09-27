// Test assignment vs access distinction
obj = {name: "John", age: 30};

// This should use dictionary access for assignment
obj.name = "Jane";
obj.age = 25;

// This should use safe attribute access for reading
name = obj.name;
console.log("Name:", name);