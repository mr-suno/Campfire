// the controller for the window
// bounces around the screen like the DVD screensaver

const windows = [];
const width = 320;
const height = 255;

let screenWidth, screenHeight;

const speed = 3;

chrome.app.runtime.onLaunched.addListener(function() {
    chrome.system.display.getInfo(function(displays) {
        const primaryDisplay = displays.find(d => d.isPrimary) || displays[0];
        screenWidth = primaryDisplay.workArea.width;
        screenHeight = primaryDisplay.workArea.height;
        
        createBouncingWindow();
        setInterval(createBouncingWindow, 1000);
    });
});

function createBouncingWindow() {
    const windowId = windows.length;

    const direction = { 
        x: (Math.random() < 0.5 ? -1 : 1) * speed, 
        y: (Math.random() < 0.5 ? -1 : 1) * speed 
    };

    chrome.app.window.create('window.html', {
        id: 'window' + windowId,
        bounds: {
            width: width,
            height: height,
            left: Math.floor(Math.random() * (screenWidth - width)),
            top: Math.floor(Math.random() * (screenHeight - height))
        }
    }, function(createdWindow) {
        windows.push({ window: createdWindow, direction: direction });

        moveWindow(windowId);
    });
}

function moveWindow(windowId) {
    const windowObj = windows[windowId];
    if (!windowObj) return;

    function updatePosition() {
        const bounds = windowObj.window.getBounds();
        let newLeft = bounds.left + windowObj.direction.x;
        let newTop = bounds.top + windowObj.direction.y;

        if (newLeft <= 0 || newLeft >= screenWidth - width) {
            windowObj.direction.x = -windowObj.direction.x;
            newLeft = Math.max(0, Math.min(newLeft, screenWidth - width));
        }

        if (newTop <= 0 || newTop >= screenHeight - height) {
            windowObj.direction.y = -windowObj.direction.y;
            newTop = Math.max(0, Math.min(newTop, screenHeight - height));
        }

        windowObj.window.setBounds({
            left: Math.round(newLeft),
            top: Math.round(newTop)
        });

        setTimeout(updatePosition, 16);
    }

    updatePosition();
}
