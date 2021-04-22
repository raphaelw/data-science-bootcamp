const socket = io(); /* no parameters, because socket server is same-origin */

socket.on("connect", () => {
    console.log(socket.connected); // true
    document.getElementById('socket_status').textContent = 'Status: Live';
});
  
socket.on("disconnect", () => {
    console.log(socket.connected); // false
    document.getElementById('socket_status').textContent = 'Status: Disconnected';
});

/* communication events */

socket.on("new_tweet", (arg) => {
    console.log(arg); // world
    //document.getElementById('out').textContent = ...;
});