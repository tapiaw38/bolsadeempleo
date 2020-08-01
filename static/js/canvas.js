var canvas = document.getElementById('canvas')
var context
var imagen;
var archivo

window.onload = (event)=>{
    canvas = document.getElementById('canvas');
    context = canvas.getContext('2d');
    archivo = document.getElementById('archivo');
}

function obtenerImagen(){

    //cargar imagen********************************************
    imagen = new Image;
    imagen.onload = ()=>{
        console.log('imagen cargada!')
        dibujarImagenes();
    }
    imagen.src = URL.createObjectURL(archivo.files[0]);
    /******************************************************* */
}

function dibujarImagenes(){

    //Parar el mainLoop anterior
    if(window.mainLoop !== null)
    {
        //console.log('PARO!')
        clearInterval(window.mainLoop)
    }

    //Dibujar imagen por primera vez**************************
    var px = (canvas.width - imagen.width) / 2//Posicion x inicial en el medio
    var py = (canvas.height - imagen.height) / 2//Posicion y inicial en el medio
    var sx = imagen.width;//tamano de imagen en x
    var sy = imagen.height;//tamano de imagen en y

    //Si la imagen es muy grande la encogemos un poco
    if(sx > 2000 || sy > 2000)
    {
        sx = sx /10
        sy = sy /10;

        px = (canvas.width - sx) / 2;
        py = (canvas.height - sy) / 2;
    }else if(sx > 1000 || sy > 1000)//Agrandamos la imagen si es muy pequena
    {
        sx = sx / 5
        sy = sy / 5;

        px = (canvas.width - sx) / 2;
        py = (canvas.height - sy) / 2;
    }else if(sx > 500 || sy > 500)//Agrandamos la imagen si es muy pequena
    {
        sx = sx / 3
        sy = sy / 3;

        px = (canvas.width - sx) / 2;
        py = (canvas.height - sy) / 2;
    }else if(sx < 100 || sy < 100)//Agrandamos la imagen si es muy pequena
    {
        sx = sx * 2
        sy = sy * 2;

        px = (canvas.width - sx) / 2;
        py = (canvas.height - sy) / 2;
    }
    context.fillStyle = 'darkgray';
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.drawImage(imagen, px, py, sx, sy);
    //****************************************************** */

    //Mover imagen:****************************************************

    /************************************************************* */

    window.mainLoop = setInterval(()=>{
        
        if(presionando == true && moviendo == true)
        {
            //Obtenemos la posicion actual del mouse el rpimer frame
            if(contador == 0)
            {
                amx = px;
                amy = py;
            }
        
            if(contador > 1)
            {
                //Calculamos la posicion delta del mouse y se lo agregamos a la posicion de la imagen
                pdx = mx - amx;
                pdy = my - amy;
                px += pdx;
                py += pdy;

                //Limpiamos el canvas y dibujamos la imagen con la nueva posicion
                context.fillStyle = 'darkgray';
                context.fillRect(0, 0, canvas.width, canvas.height);
                context.drawImage(imagen, px, py, sx, sy);
                
            }
            amx = mx;
            amy = my;
            contador++;
        }
    }, 1000/60)//60 = 60FPS
    /************************************************************** */

    //Resizar imagen
    var porcentajeResizado = 0.1;//Se usa para scalar la imagen sin perder el aspect ratio
    canvas.onmousewheel = (event)=>{
        if(event.deltaY == 100)
        {
            //console.log('para abajo')
            //limitamos al usuario para que no haga la imagen demasiado pequena
            if(sx > canvas.width || sy > sy.height)
            {
                //Calcular el nuevo size de la imagen y ponerla en el centro
                sx -= sx * porcentajeResizado;
                sy -= sy * porcentajeResizado;
                px = (canvas.width - sx) / 2;
                py = (canvas.height - sy) / 2;
                /******************************************************** */
                context.fillStyle = 'darkgray';
                context.fillRect(0, 0, canvas.width, canvas.height);
                context.drawImage(imagen, px, py, sx, sy);
            }
            
        }else
        {
            //Calcular el nuevo size de la imagen y ponerla en el centro
            sx += sx * porcentajeResizado;
            sy += sy * porcentajeResizado;
            px = (canvas.width - sx) / 2;
            py = (canvas.height - sy) / 2;
            /********************************************************** */
            context.fillStyle = 'darkgray';
            context.fillRect(0, 0, canvas.width, canvas.height);
            context.drawImage(imagen, px, py, sx, sy);
            //console.log('para arriba');
        }
        //console.log(event);
    }

    
}

function mostrarResultado(){
    var imagenAMostrar = document.getElementById('imagenMostrada');
    canvas.toBlob((blob)=>{
        imagenAMostrar.setAttribute('src', URL.createObjectURL(blob));
        imagenAMostrar.style.display = 'block';
    })
}
