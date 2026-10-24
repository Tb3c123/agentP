#!/usr/bin/env python3
"""
agentP - Native macOS .app & .dmg Automated Build & Packaging Pipeline
Author: Liam (DevOps Lead) & Lucas (Senior Dev) & Alex (Lead PM)
"""

import os
import sys
import subprocess
import shutil
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIST_DIR = os.path.join(BASE_DIR, 'dist')
APP_BUNDLE = os.path.join(DIST_DIR, 'agentP.app')
CONTENTS_DIR = os.path.join(APP_BUNDLE, 'Contents')
MACOS_DIR = os.path.join(CONTENTS_DIR, 'MacOS')
RESOURCES_DIR = os.path.join(CONTENTS_DIR, 'Resources')
DMG_STAGING = os.path.join(DIST_DIR, 'dmg_staging')
OUTPUT_DMG = os.path.join(DIST_DIR, 'agentP-v2.9.0-macOS-arm64.dmg')

def step(title: str):
    print(f"\n===> {title}")

def run(cmd: str, check=True):
    print(f"$ {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=BASE_DIR)
    if check and res.returncode != 0:
        print(f"Error executing command: {cmd}")
        sys.exit(res.returncode)
    return res.returncode

def main():
    print("=================================================================")
    print("🍎 agentP NATIVE macOS .APP & .DMG PRODUCTION BUILD PIPELINE")
    print("=================================================================")

    # 1. Prepare clean directories
    step("1. Preparing clean distribution directories")
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(MACOS_DIR, exist_ok=True)
    os.makedirs(RESOURCES_DIR, exist_ok=True)
    os.makedirs(DMG_STAGING, exist_ok=True)

    # 2. Generate Apple .icns Icon
    step("2. Generating Apple Iconset and AppIcon.icns")
    iconset_dir = os.path.join(DIST_DIR, 'AppIcon.iconset')
    os.makedirs(iconset_dir, exist_ok=True)

    # Compile AppKit icon generator
    icon_gen_c = os.path.join(DIST_DIR, 'gen_icon.m')
    with open(icon_gen_c, 'w') as f:
        f.write('''#import <Cocoa/Cocoa.h>
int main() {
    NSBitmapImageRep *rep = [[NSBitmapImageRep alloc] initWithBitmapDataPlanes:NULL
        pixelsWide:1024 pixelsHigh:1024 bitsPerSample:8 samplesPerPixel:4 hasAlpha:YES
        isPlanar:NO colorSpaceName:NSCalibratedRGBColorSpace bytesPerRow:0 bitsPerPixel:0];
    [NSGraphicsContext saveGraphicsState];
    [NSGraphicsContext setCurrentContext:[NSGraphicsContext graphicsContextWithBitmapImageRep:rep]];
    
    // Background: Rounded squircle in Alpine Teal #0D9488
    NSColor *teal = [NSColor colorWithCalibratedRed:13.0/255.0 green:148.0/255.0 blue:136.0/255.0 alpha:1.0];
    [teal setFill];
    NSBezierPath *path = [NSBezierPath bezierPathWithRoundedRect:NSMakeRect(40, 40, 944, 944) xRadius:220 yRadius:220];
    [path fill];
    
    // Tuscan Amber visor accent #D97706
    NSColor *amber = [NSColor colorWithCalibratedRed:217.0/255.0 green:119.0/255.0 blue:6.0/255.0 alpha:1.0];
    [amber setFill];
    NSBezierPath *visor = [NSBezierPath bezierPathWithRoundedRect:NSMakeRect(280, 720, 464, 90) xRadius:45 yRadius:45];
    [visor fill];

    // White monogram 'P'
    NSDictionary *attrs = @{
        NSFontAttributeName: [NSFont boldSystemFontOfSize:620],
        NSForegroundColorAttributeName: [NSColor whiteColor]
    };
    NSString *text = @"P";
    NSSize size = [text sizeWithAttributes:attrs];
    [text drawAtPoint:NSMakePoint((1024 - size.width)/2.0, (1024 - size.height)/2.0 - 50) withAttributes:attrs];
    
    [NSGraphicsContext restoreGraphicsState];
    NSData *pngData = [rep representationUsingType:NSBitmapImageFileTypePNG properties:@{}];
    [pngData writeToFile:@"dist/master_icon.png" atomically:YES];
    return 0;
}
''')
    run(f"clang -framework Cocoa {icon_gen_c} -o dist/gen_icon && dist/gen_icon")

    # Generate standard icon sizes
    sizes = [16, 32, 64, 128, 256, 512]
    for s in sizes:
        run(f"sips -z {s} {s} dist/master_icon.png --out {iconset_dir}/icon_{s}x{s}.png > /dev/null")
        if s * 2 <= 1024:
            run(f"sips -z {s*2} {s*2} dist/master_icon.png --out {iconset_dir}/icon_{s}x{s}@2x.png > /dev/null")
    run(f"sips -z 1024 1024 dist/master_icon.png --out {iconset_dir}/icon_512x512@2x.png > /dev/null")

    # Compile iconset to icns
    icns_path = os.path.join(RESOURCES_DIR, 'AppIcon.icns')
    run(f"iconutil -c icns {iconset_dir} -o {icns_path}")
    print(f"✓ Created {icns_path}")

    # 3. Compile Native macOS Cocoa & WebKit Binary
    step("3. Compiling native macOS Cocoa & WebKit application binary")
    native_src = os.path.join(BASE_DIR, 'src-tauri', 'native_mac', 'main.m')
    exec_path = os.path.join(MACOS_DIR, 'agentP')
    run(f"clang -O3 -framework Cocoa -framework WebKit {native_src} -o {exec_path}")
    run(f"chmod +x {exec_path}")
    print(f"✓ Native binary compiled: {exec_path}")

    # 4. Create Info.plist
    step("4. Generating bundle Info.plist")
    plist_path = os.path.join(CONTENTS_DIR, 'Info.plist')
    with open(plist_path, 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>agentP</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.agentp.desktop</string>
    <key>CFBundleName</key>
    <string>agentP</string>
    <key>CFBundleDisplayName</key>
    <string>agentP</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>2.9.0</string>
    <key>CFBundleVersion</key>
    <string>2.9.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>12.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <true/>
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
        <key>NSAllowsLocalNetworking</key>
        <true/>
    </dict>
</dict>
</plist>
''')
    print(f"✓ Created {plist_path}")

    # 5. Build Apple Disk Image (.dmg)
    step("5. Building macOS Apple Disk Image (DMG)")
    shutil.copytree(APP_BUNDLE, os.path.join(DMG_STAGING, 'agentP.app'), symlinks=True)
    run(f"ln -s /Applications {DMG_STAGING}/Applications")

    # Use hdiutil to create UDZO compressed DMG
    if os.path.exists(OUTPUT_DMG):
        os.remove(OUTPUT_DMG)

    run(f'hdiutil create -volname "agentP" -srcfolder "{DMG_STAGING}" -ov -format UDZO "{OUTPUT_DMG}"')
    dmg_size_mb = round(os.path.getsize(OUTPUT_DMG) / (1024 * 1024), 2)
    print(f"✓ SUCCESS: Created {OUTPUT_DMG} ({dmg_size_mb} MB)")

    # 6. Verify DMG structure
    step("6. Verifying DMG Image Structure")
    run(f'hdiutil imageinfo "{OUTPUT_DMG}" | grep -E "Format|Total Bytes"')

    print("\n=================================================================")
    print(f"🎉 agentP macOS DMG BUILD COMPLETE!")
    print(f"📁 Bundle: {APP_BUNDLE}")
    print(f"💿 DMG:    {OUTPUT_DMG} ({dmg_size_mb} MB)")
    print("=================================================================")

if __name__ == '__main__':
    main()
