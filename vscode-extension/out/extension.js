"use strict";
// SkillGate VSCode Extension
// src/extension.ts
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const child_process_1 = require("child_process");
let diagnosticCollection;
function activate(context) {
    console.log('SkillGate extension activated');
    diagnosticCollection = vscode.languages.createDiagnosticCollection('skillgate');
    context.subscriptions.push(diagnosticCollection);
    // Command: Scan current file
    let scanFile = vscode.commands.registerCommand('skillgate.scanFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor)
            return;
        const fileUri = editor.document.uri;
        await runSkillGateScan(fileUri.fsPath);
        vscode.window.showInformationMessage('SkillGate: Scan complete');
    });
    // Command: Scan workspace
    let scanWorkspace = vscode.commands.registerCommand('skillgate.scanWorkspace', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders)
            return;
        for (const folder of workspaceFolders) {
            await runSkillGateScan(folder.uri.fsPath);
        }
        vscode.window.showInformationMessage('SkillGate: Workspace scan complete');
    });
    // Command: Show dashboard
    let showDashboard = vscode.commands.registerCommand('skillgate.showDashboard', () => {
        const panel = vscode.window.createWebviewPanel('skillgateDashboard', 'SkillGate Dashboard', vscode.ViewColumn.One, {});
        panel.webview.html = getDashboardHtml();
    });
    context.subscriptions.push(scanFile, scanWorkspace, showDashboard);
    // Auto-scan on save
    vscode.workspace.onDidSaveTextDocument(async (doc) => {
        const config = vscode.workspace.getConfiguration('skillgate');
        if (config.get('autoScanOnSave')) {
            await runSkillGateScan(doc.uri.fsPath);
        }
    });
}
async function runSkillGateScan(filePath) {
    const skillgatePath = vscode.workspace.getConfiguration('skillgate').get('path', 'skillgate');
    return new Promise((resolve) => {
        (0, child_process_1.execFile)(skillgatePath, ['scan', filePath, '--format', 'json'], (error, stdout, stderr) => {
            try {
                const result = JSON.parse(stdout);
                updateDiagnostics(result, filePath);
            }
            catch (e) {
                console.error('SkillGate scan failed:', e);
            }
            resolve(undefined);
        });
    });
}
function updateDiagnostics(result, filePath) {
    const diagnostics = [];
    for (const finding of result.findings || []) {
        const severity = finding.severity === 'CRITICAL' || finding.severity === 'HIGH'
            ? vscode.DiagnosticSeverity.Error
            : finding.severity === 'MEDIUM'
                ? vscode.DiagnosticSeverity.Warning
                : vscode.DiagnosticSeverity.Information;
        const range = new vscode.Range((finding.line || 1) - 1, 0, (finding.line || 1) - 1, 100);
        diagnostics.push(new vscode.Diagnostic(range, `[SkillGate] ${finding.category}: ${finding.message}`, severity));
    }
    diagnosticCollection.set(vscode.Uri.file(filePath), diagnostics);
}
function getDashboardHtml() {
    return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SkillGate Dashboard</title>
    <style>
        body { font-family: -apple-system, sans-serif; padding: 20px; }
        .stat { background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>🛡️ SkillGate Dashboard</h1>
    <div class="stat">
        <h2>Trust Score</h2>
        <p>Run a scan to see your score.</p>
    </div>
</body>
</html>`;
}
function deactivate() {
    if (diagnosticCollection) {
        diagnosticCollection.dispose();
    }
}
//# sourceMappingURL=extension.js.map