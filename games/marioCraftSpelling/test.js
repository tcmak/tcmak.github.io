#!/usr/bin/env node

/**
 * MarioCraft Headless Test Runner
 * Executes all 27 unit test suites embedded in index.html.
 */

const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const scriptContent = html.split('<script>')[1].split('</script>')[0];

// Mock browser APIs required for headless execution
const mockLocalStorage = {};
global.localStorage = {
    getItem: k => mockLocalStorage[k] || null,
    setItem: (k, v) => { mockLocalStorage[k] = String(v); },
    removeItem: k => { delete mockLocalStorage[k]; },
    clear: () => { Object.keys(mockLocalStorage).forEach(k => delete mockLocalStorage[k]); }
};

global.window = {
    AudioContext: class {
        createOscillator() { return { connect: () => {}, start: () => {}, stop: () => {}, frequency: { setValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} } }; }
        createGain() { return { connect: () => {}, gain: { setValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} } }; }
        get destination() { return {}; }
        get currentTime() { return 0; }
    },
    addEventListener: () => {},
    location: { search: '?test=true' },
    speechSynthesis: { cancel: () => {}, speak: () => {} }
};

global.SpeechSynthesisUtterance = class { constructor(t) { this.text = t; } };

let report = '';
global.document = {
    getElementById: (id) => ({
        width: 800,
        height: 448,
        getContext: () => ({
            fillRect: () => {}, strokeRect: () => {}, clearRect: () => {},
            fillText: () => {}, save: () => {}, restore: () => {}
        }),
        classList: { add: () => {}, remove: () => {} },
        style: {},
        addEventListener: () => {},
        set innerText(v) { report = v; },
        innerHTML: ''
    }),
    createElement: () => ({ className: '' })
};

global.fetch = async (url) => {
    return {
        json: async () => JSON.parse(fs.readFileSync(path.join(__dirname, url), 'utf8'))
    };
};

try {
    eval(scriptContent);
    // Wait for async fetch to finish and tests to run
    const startTime = Date.now();
    const interval = setInterval(() => {
        if (report.length > 0 || Date.now() - startTime > 3000) {
            clearInterval(interval);
            const passCount = (report.match(/PASS:/g) || []).length;
            console.log(report);
            if (report.includes('MINI UNIT TESTS PASSED SUCCESSFULLY')) {
                console.log(`\x1b[32m✔ All ${passCount} assertions passed across unit test categories!\x1b[0m\n`);
                process.exit(0);
            } else {
                console.error('\x1b[31m✖ Tests failed!\x1b[0m\n');
                process.exit(1);
            }
        }
    }, 50);
} catch (err) {
    console.error('\x1b[31mExecution Error during tests:\x1b[0m', err);
    process.exit(1);
}
