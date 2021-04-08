// CANVAS VARIABLES
CANVAS_WIDTH = 320
CANVAS_HEIGHT = 450

// GRAPH VARIABLES
MARGIN_WIDTH = 65
MARGIN_HEIGHT = 20

// DEFINITIONS FOR THE GRAPH - RIGHT HORIZONTAL LINE
START_RIGHT_LINES = MARGIN_WIDTH-5
WIDTH_LINES = 8

// DEFINITIONS FOR THE GRAPH - LEFT HORIZONTAL LINE
START_LEFT_LINES = MARGIN_WIDTH-12.5

// DEFINITONS FOR THE IMAGE
TURTLE_WIDTH = 50
TURTLE_HEIGHT = 40

// DEFINITIONS FOR THE LABELS TEXT
RIGHT_TEXT_OFFSET = -13 // higher the text goes left
LEFT_TEXT_OFFSET = 5
UP_OFFSET_LEFT_TEXT = 8
UP_OFFSET_RIGTH_TEXT = 5

// DEFINITIONS FOR THE LABELS
// or 135 OR LAYERS_LEVEL[0]
RECT_LAYERS_START = 80
RECT_LAYERS_HEIGHT = 30 //before 35

OFFSET_RECT_LAYERS_HEIGHT = 1

LAYERS_OFFSET = 2

LAYERS_LEVEL = []

function widthMargin(){
    return CANVAS_WIDTH - (MARGIN_WIDTH*2)
}
function heightMargin(){
    return CANVAS_HEIGHT - (MARGIN_HEIGHT*2)

}
function widthMarginLine(){
    return CANVAS_WIDTH + (-START_RIGHT_LINES)
}

var range = n => Array(n + 1).join(1).split('').map((x, i) => i)


window.addEventListener('load', () => {
    const canvas = document.querySelector('#canvas');
    const context = canvas.getContext('2d'); //'#c9f2e7'
    //For Images in the js file, assign the path in the dashboard_graphs.html first
    const background_img = document.getElementById('background_img_source');
    const turtle_img = document.getElementById('turtle_img_source');

    //Resizing
    canvas.width = CANVAS_WIDTH;
    canvas.height = CANVAS_HEIGHT;    

    // Draw Background Image ----------------------------------------------------------------
    context.drawImage(background_img_source, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
    //context.globalCompositeOperation = 'destination-atop';
    
    
    // define layers start rectangles
    for (const index in range(13)) {
        LAYERS_LEVEL.push(RECT_LAYERS_START + (RECT_LAYERS_HEIGHT+1)*index)
        }

    function drawLayer(color, i, meters_deep) {
        // Layers Rectangles
        context.lineWidth = 2;
        context.fillStyle = color;
        context.fillRect(MARGIN_WIDTH+LAYERS_OFFSET, LAYERS_LEVEL[i], widthMargin() - LAYERS_OFFSET*1.5, RECT_LAYERS_HEIGHT+OFFSET_RECT_LAYERS_HEIGHT);
        
        // Draw Turtle Image ----------------------------------------------------------------
        context.drawImage(turtle_img, CANVAS_WIDTH/2 - TURTLE_WIDTH/2+3, LAYERS_LEVEL[0] + RECT_LAYERS_HEIGHT/2 - TURTLE_HEIGHT/2, TURTLE_WIDTH, TURTLE_HEIGHT)

        // drawHorizontalLine
        // Right Side        
        context.lineWidth = 3;
        context.strokeStyle = "black";
        if (i <= 10) {
            context.beginPath();
            context.moveTo(widthMarginLine(), LAYERS_LEVEL[i]);
            context.lineTo(widthMarginLine()+WIDTH_LINES, LAYERS_LEVEL[i]);            
            context.stroke();
        }
        // Left Side
        context.beginPath();
        context.moveTo(START_LEFT_LINES, LAYERS_LEVEL[i]);
        context.lineTo(START_LEFT_LINES+WIDTH_LINES, LAYERS_LEVEL[i]);            
        context.stroke();
        
        // drawVerticalLine
        if (i != 11) {
            //context.lineWidth = 3;
            //context.strokeStyle = "black";
            // Right Side
            if (i <= 9) {
                context.beginPath();
                context.moveTo(widthMarginLine()+WIDTH_LINES, LAYERS_LEVEL[i]);
                context.lineTo(widthMarginLine()+WIDTH_LINES, LAYERS_LEVEL[i+1]);            
                context.stroke();
            }
            // Left Side
            context.beginPath();
            context.moveTo(START_LEFT_LINES, LAYERS_LEVEL[i]);
            context.lineTo(START_LEFT_LINES, LAYERS_LEVEL[i+1]);       
            context.stroke();
        }
        for (const index in range(2)) {   // to draw darker     
            // Draw Left Text
            //context.font = "30px Verdana"; Arial Georgia
            //context.strokeText("Big smile!", 10, 50);
            var lineheight = 15;
            context.font = "bold 10.4px Georgia";
            context.fillStyle = "black";
            if (i <= 8) {
                var txt = " meters"            
                context.fillText('  ' + meters_deep, START_LEFT_LINES - LEFT_TEXT_OFFSET - context.measureText(txt).width, LAYERS_LEVEL[i]+1 + lineheight/2);
                context.fillText(txt, START_LEFT_LINES - LEFT_TEXT_OFFSET - context.measureText(txt).width, LAYERS_LEVEL[i]+1 + lineheight/0.8);
            }
            else if (i == 9) {
                var txt = " meters"
                context.fillText(meters_deep, START_LEFT_LINES - LEFT_TEXT_OFFSET - context.measureText(meters_deep).width, LAYERS_LEVEL[i]+1 + lineheight/2);
                context.fillText(txt, START_LEFT_LINES - LEFT_TEXT_OFFSET - context.measureText(txt).width, LAYERS_LEVEL[i]+1 + lineheight/0.8);
            }
            else if (i == 10) {
                var below = " below"
                var txt = " meters"
                context.fillText(below, START_LEFT_LINES - LEFT_TEXT_OFFSET - context.measureText(txt).width, LAYERS_LEVEL[i]-2 + lineheight*2/3.5);
                context.fillText('  ' + meters_deep, START_LEFT_LINES - LEFT_TEXT_OFFSET - context.measureText(txt).width, LAYERS_LEVEL[i]+1 + lineheight);
                context.fillText(txt, START_LEFT_LINES - LEFT_TEXT_OFFSET - context.measureText(txt).width, LAYERS_LEVEL[i]-2 + lineheight*2/1.05);
            }
            else {
                context.fillText(' ' + meters_deep, START_LEFT_LINES - LEFT_TEXT_OFFSET-1 - context.measureText(meters_deep).width, LAYERS_LEVEL[i] + lineheight*1.2);            
            }

            // Draw Rigth Text
            if (i <= 10) {
                if (i <=9) {
                    context.fillText('Layer '+ (i+1), widthMarginLine()-RIGHT_TEXT_OFFSET, LAYERS_LEVEL[i] + UP_OFFSET_RIGTH_TEXT + lineheight);
                }
            }
        }
        
        // Draw Border of the Graph
        context.lineWidth = 3;
        context.strokeStyle = "black";
        context.strokeRect(MARGIN_WIDTH, MARGIN_HEIGHT, widthMargin(), LAYERS_LEVEL[LAYERS_LEVEL.length - 1] - RECT_LAYERS_HEIGHT + ((OFFSET_RECT_LAYERS_HEIGHT*i+2)/2));
        

        


        //const image = new Image(TURTLE_WIDTH, TURTLE_HEIGHT); // Using optional size for image
        //image.onload = drawImageActualSize; // Function - Draw when image has loaded

        // Load an image of intrinsic size 300x227 in CSS pixels
        //image.src = 'https://mdn.mozillademos.org/files/5397/rhino.jpg';
        //var turtle_url = "{% static 'img/{}.turtle_right.png' %}";
        //image.src = turtle_img

        //function drawImageActualSize() {
            // Use the intrinsic size of image in CSS pixels for the canvas element
            //canvas.width = this.naturalWidth;
            //canvas.height = this.naturalHeight;

            // Will draw the image as 300x227, ignoring the custom size of 60x45
            // given in the constructor
            //context.drawImage(this, 0, 0);

            // To use the custom size we'll have to specify the scale parameters
            // using the element's width and height properties - lets draw one
            // on top in the corner:
            //context.drawImage(this, 0, 0, this.width, this.height);
        //}
        
    }

    drawLayer('#c9f2e7', 0, "0 - 5")
    drawLayer('#a5e1e7', 1, "6-10")
    drawLayer('#75c8dc', 2, "11-20")
    drawLayer('#41b2dc', 3, "21-30")
    drawLayer('#1d9af2', 4, "31-40")
    drawLayer('#0078f2', 5, "41-50")
    drawLayer('#005df2', 6, "51-70")
    drawLayer('#093aff', 7, "71-90")
    drawLayer('#091bff', 8, "91-110")
    drawLayer('#0014cc', 9, "111-4095")
    drawLayer('#0502b0', 10, "4096")
    drawLayer('#5e512e', 11, "Seabed")     
})