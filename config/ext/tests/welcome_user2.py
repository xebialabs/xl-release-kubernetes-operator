context.logOutput("Hello " + user)
myval = context.getAttribute("myattr")
print("I am user1 " + myval)
if( myval != user ):
    raise error('I expected ' + user + ' but I got ' + myval)