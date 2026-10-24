#import <Cocoa/Cocoa.h>
#import <WebKit/WebKit.h>
#import <sys/socket.h>
#import <netinet/in.h>
#import <arpa/inet.h>
#import <unistd.h>

@interface AppDelegate : NSObject <NSApplicationDelegate, NSWindowDelegate, WKNavigationDelegate>
@property (strong, nonatomic) NSWindow *window;
@property (strong, nonatomic) WKWebView *webView;
@property (strong, nonatomic) NSTask *daemonTask;
@end

@implementation AppDelegate

- (BOOL)isDaemonRunningOnPort:(int)port {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return NO;
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port);
    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);

    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = 200000; // 200ms timeout
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv);
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (const char*)&tv, sizeof tv);

    int res = connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    close(sock);
    return (res == 0);
}

- (void)startLocalDaemonIfNeeded {
    if ([self isDaemonRunningOnPort:9090]) {
        NSLog(@"[agentP macOS Shell] Local daemon is already running at port 9090.");
        return;
    }

    NSLog(@"[agentP macOS Shell] Starting agentP Core Python Daemon...");
    // Find project root directory relative to .app bundle or current working dir
    NSString *bundlePath = [[NSBundle mainBundle] bundlePath];
    NSString *projectRoot = [bundlePath stringByDeletingLastPathComponent];
    
    // Check if router.py is in projectRoot or bundle resources
    NSString *routerPath = [projectRoot stringByAppendingPathComponent:@"src/daemon/router.py"];
    if (![[NSFileManager defaultManager] fileExistsAtPath:routerPath]) {
        // Fallback: check current directory
        routerPath = @"src/daemon/router.py";
    }

    if ([[NSFileManager defaultManager] fileExistsAtPath:routerPath]) {
        self.daemonTask = [[NSTask alloc] init];
        self.daemonTask.launchPath = @"/usr/bin/python3";
        self.daemonTask.arguments = @[routerPath];
        self.daemonTask.currentDirectoryPath = projectRoot;
        @try {
            [self.daemonTask launch];
            NSLog(@"[agentP macOS Shell] Daemon launched with PID: %d", [self.daemonTask processIdentifier]);
            usleep(400000); // 400ms wait for socket to bind
        } @catch (NSException *exception) {
            NSLog(@"[agentP macOS Shell] Exception launching daemon: %@", exception);
        }
    }
}

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    // 1. Force Clean Light Appearance (Strictly NO Dark Mode)
    if (@available(macOS 10.14, *)) {
        [NSApp setAppearance:[NSAppearance appearanceNamed:NSAppearanceNameAqua]];
    }

    // 2. Start Python daemon if needed
    [self startLocalDaemonIfNeeded];

    // 3. Create Modern Window (1440x900)
    NSRect screenRect = [[NSScreen mainScreen] visibleFrame];
    CGFloat width = 1440;
    CGFloat height = 900;
    if (width > screenRect.size.width) width = screenRect.size.width - 40;
    if (height > screenRect.size.height) height = screenRect.size.height - 40;

    NSRect frame = NSMakeRect((screenRect.size.width - width) / 2, (screenRect.size.height - height) / 2, width, height);
    NSWindowStyleMask style = NSWindowStyleMaskTitled |
                              NSWindowStyleMaskClosable |
                              NSWindowStyleMaskMiniaturizable |
                              NSWindowStyleMaskResizable |
                              NSWindowStyleMaskFullSizeContentView;

    self.window = [[NSWindow alloc] initWithContentRect:frame
                                              styleMask:style
                                                backing:NSBackingStoreBuffered
                                                  defer:NO];
    self.window.title = @"agentP — Developer Multi-Agent Platform";
    self.window.minSize = NSMakeSize(1024, 700);
    self.window.titleVisibility = NSWindowTitleHidden;
    self.window.titlebarAppearsTransparent = YES;
    self.window.backgroundColor = [NSColor colorWithCalibratedRed:248.0/255.0 green:250.0/255.0 blue:252.0/255.0 alpha:1.0]; // #F8FAFC
    self.window.delegate = self;

    // 4. Configure WKWebView
    WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
    config.preferences.javaScriptCanOpenWindowsAutomatically = YES;

    self.webView = [[WKWebView alloc] initWithFrame:self.window.contentView.bounds configuration:config];
    self.webView.autoresizingMask = NSViewWidthSizable | NSViewHeightSizable;
    self.webView.navigationDelegate = self;
    self.webView.layer.backgroundColor = CGColorCreateGenericRGB(248.0/255.0, 250.0/255.0, 252.0/255.0, 1.0);

    [self.window.contentView addSubview:self.webView];

    // 5. Load agentP Local Web Application
    NSURL *url = [NSURL URLWithString:@"http://127.0.0.1:9090"];
    NSURLRequest *req = [NSURLRequest requestWithURL:url];
    [self.webView loadRequest:req];

    [self.window makeKeyAndOrderFront:nil];
    [NSApp activateIgnoringOtherApps:YES];
    NSLog(@"[agentP macOS Shell] Native window initialized successfully.");
}

- (void)webView:(WKWebView *)webView didFailProvisionalNavigation:(WKNavigation *)navigation withError:(NSError *)error {
    NSLog(@"[agentP macOS Shell] Navigation error: %@", error.localizedDescription);
    // If daemon just started, retry in 500ms
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(500 * NSEC_PER_MSEC)), dispatch_get_main_queue(), ^{
        NSURL *url = [NSURL URLWithString:@"http://127.0.0.1:9090"];
        [self.webView loadRequest:[NSURLRequest requestWithURL:url]];
    });
}

- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)sender {
    return YES;
}

- (void)applicationWillTerminate:(NSNotification *)notification {
    if (self.daemonTask && [self.daemonTask isRunning]) {
        NSLog(@"[agentP macOS Shell] Terminating daemon process...");
        [self.daemonTask terminate];
    }
}

@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSApplication *app = [NSApplication sharedApplication];
        AppDelegate *delegate = [[AppDelegate alloc] init];
        app.delegate = delegate;

        // Build Menu Bar
        NSMenu *mainMenu = [[NSMenu alloc] init];
        NSMenuItem *appMenuItem = [[NSMenuItem alloc] init];
        [mainMenu addItem:appMenuItem];

        NSMenu *appMenu = [[NSMenu alloc] initWithTitle:@"agentP"];
        [appMenu addItemWithTitle:@"About agentP" action:nil keyEquivalent:@""];
        [appMenu addItem:[NSMenuItem separatorItem]];
        [appMenu addItemWithTitle:@"Hide agentP" action:@selector(hide:) keyEquivalent:@"h"];
        [appMenu addItemWithTitle:@"Hide Others" action:@selector(hideOtherApplications:) keyEquivalent:@"h"];
        [appMenu addItem:[NSMenuItem separatorItem]];
        [appMenu addItemWithTitle:@"Quit agentP" action:@selector(terminate:) keyEquivalent:@"q"];
        [appMenuItem setSubmenu:appMenu];

        // Edit Menu (For copy/paste in web inputs)
        NSMenuItem *editMenuItem = [[NSMenuItem alloc] init];
        [mainMenu addItem:editMenuItem];
        NSMenu *editMenu = [[NSMenu alloc] initWithTitle:@"Edit"];
        [editMenu addItemWithTitle:@"Undo" action:@selector(undo:) keyEquivalent:@"z"];
        [editMenu addItemWithTitle:@"Redo" action:@selector(redo:) keyEquivalent:@"Z"];
        [editMenu addItem:[NSMenuItem separatorItem]];
        [editMenu addItemWithTitle:@"Cut" action:@selector(cut:) keyEquivalent:@"x"];
        [editMenu addItemWithTitle:@"Copy" action:@selector(copy:) keyEquivalent:@"c"];
        [editMenu addItemWithTitle:@"Paste" action:@selector(paste:) keyEquivalent:@"v"];
        [editMenu addItemWithTitle:@"Select All" action:@selector(selectAll:) keyEquivalent:@"a"];
        [editMenuItem setSubmenu:editMenu];

        [app setMainMenu:mainMenu];

        [app run];
    }
    return 0;
}
