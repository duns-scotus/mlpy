/**
 * Debug Adapter for ML Language
 *
 * This module provides VS Code debug adapter integration for ML programs.
 * It spawns the Python DAP server and connects it to VS Code's debugging UI.
 *
 * Architecture:
 *   VS Code (Debug UI) <-> debugAdapter.ts <-> dap_server.py <-> MLDebugger
 */

import * as vscode from 'vscode';
import * as path from 'path';

/**
 * Debug adapter descriptor factory for ML language.
 *
 * This factory creates debug sessions by spawning the Python DAP server
 * and connecting it to VS Code via the Debug Adapter Protocol.
 */
export class MLDebugAdapterDescriptorFactory implements vscode.DebugAdapterDescriptorFactory {

    /**
     * Create debug adapter descriptor for a debug session.
     *
     * @param session Debug session configuration
     * @param executable Optional debug adapter executable (not used)
     * @returns Debug adapter descriptor connecting to DAP server
     */
    createDebugAdapterDescriptor(
        session: vscode.DebugSession,
        executable: vscode.DebugAdapterExecutable | undefined
    ): vscode.ProviderResult<vscode.DebugAdapterDescriptor> {

        // Get configuration
        const config = session.configuration;
        const pythonPath = config.pythonPath || this.getPythonPath();
        const mlpyPath = config.mlpyPath || this.getMLPyPath();

        console.log(`[ML Debug] Launching DAP server: ${pythonPath} -m src.mlpy.cli.app debug-adapter`);

        // Prepare arguments for DAP server (use full module path to avoid import issues)
        const args = ['-m', 'src.mlpy.cli.app', 'debug-adapter'];
        if (config.trace) {
            args.push('--log');
        }

        // Prepare options
        const options: vscode.DebugAdapterExecutableOptions = {
            cwd: mlpyPath,
            env: {
                ...process.env,
                PYTHONPATH: mlpyPath
            }
        };

        // Return executable descriptor - VS Code will spawn the process
        return new vscode.DebugAdapterExecutable(pythonPath, args, options);
    }

    /**
     * Get Python interpreter path from VS Code settings.
     *
     * @returns Python executable path
     */
    private getPythonPath(): string {
        // Try to get Python path from VS Code Python extension settings
        const config = vscode.workspace.getConfiguration('python');
        let pythonPath = config.get<string>('defaultInterpreterPath') ||
                         config.get<string>('pythonPath') ||
                         'python';

        // On Windows, try common Python locations if default not found
        if (process.platform === 'win32' && pythonPath === 'python') {
            const commonPaths = [
                'python.exe',
                'py.exe',
                'C:\\Python312\\python.exe',
                'C:\\Python311\\python.exe',
                'C:\\Python310\\python.exe',
                'C:\\Python39\\python.exe'
            ];

            for (const tryPath of commonPaths) {
                try {
                    require('child_process').execSync(`${tryPath} --version`, { stdio: 'ignore' });
                    pythonPath = tryPath;
                    break;
                } catch (e) {
                    // Continue trying
                }
            }
        }

        return pythonPath;
    }

    /**
     * Get mlpy project root path.
     *
     * @returns Project root directory path
     */
    private getMLPyPath(): string {
        // Get workspace folder
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (workspaceFolders && workspaceFolders.length > 0) {
            return workspaceFolders[0].uri.fsPath;
        }

        // Fallback to current directory
        return process.cwd();
    }
}

/**
 * Debug configuration provider for ML language.
 *
 * Provides default debug configurations and resolves configurations
 * before starting a debug session.
 */
class MLDebugConfigurationProvider implements vscode.DebugConfigurationProvider {

    /**
     * Provide default launch configuration when none exists.
     *
     * @param folder Workspace folder
     * @returns Array of default debug configurations
     */
    provideDebugConfigurations(
        folder: vscode.WorkspaceFolder | undefined
    ): vscode.ProviderResult<vscode.DebugConfiguration[]> {

        return [
            {
                type: 'ml',
                request: 'launch',
                name: 'Debug Current ML File',
                program: '${file}',
                stopOnEntry: false
            },
            {
                type: 'ml',
                request: 'launch',
                name: 'Debug ML File with Args',
                program: '${file}',
                args: [],
                stopOnEntry: false
            },
            {
                type: 'ml',
                request: 'launch',
                name: 'Debug and Stop on Entry',
                program: '${file}',
                stopOnEntry: true
            }
        ];
    }

    /**
     * Resolve and validate debug configuration before starting session.
     *
     * @param folder Workspace folder
     * @param config Debug configuration
     * @param token Cancellation token
     * @returns Resolved debug configuration or undefined to cancel
     */
    resolveDebugConfiguration(
        folder: vscode.WorkspaceFolder | undefined,
        config: vscode.DebugConfiguration,
        token?: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.DebugConfiguration> {

        // Debug logging
        console.log('[ML Debug] resolveDebugConfiguration called');
        console.log('[ML Debug] config.program BEFORE:', config.program);
        console.log('[ML Debug] folder:', folder?.uri.fsPath);

        // If launching without configuration (F5 without launch.json)
        if (!config.type && !config.request && !config.name) {
            const editor = vscode.window.activeTextEditor;

            if (editor && editor.document.languageId === 'ml') {
                // Create quick debug configuration for active ML file
                return {
                    type: 'ml',
                    request: 'launch',
                    name: 'Debug Current File',
                    program: editor.document.uri.fsPath,
                    stopOnEntry: false
                };
            } else {
                vscode.window.showErrorMessage('No ML file selected. Please open an ML file to debug.');
                return undefined;
            }
        }

        // If no program specified, use active editor
        if (!config.program) {
            const editor = vscode.window.activeTextEditor;

            if (editor && editor.document.languageId === 'ml') {
                config.program = editor.document.uri.fsPath;
            } else {
                vscode.window.showErrorMessage('Cannot debug: No ML file selected.');
                return undefined;
            }
        }

        // Resolve relative paths (check for both Unix and Windows absolute paths)
        if (config.program) {
            // Don't resolve if it contains VS Code variables (${...})
            const hasVSCodeVariable = config.program.includes('${');

            if (!hasVSCodeVariable) {
                // Windows absolute paths start with drive letter (C:\) or UNC (\\)
                // Unix absolute paths start with /
                const isWindowsAbsolute = /^[a-zA-Z]:\\/.test(config.program) || config.program.startsWith('\\\\');
                const isUnixAbsolute = config.program.startsWith('/');

                if (!isWindowsAbsolute && !isUnixAbsolute && folder) {
                    // It's a relative path, resolve it
                    config.program = path.join(folder.uri.fsPath, config.program);
                }
            }
            // If it has VS Code variables, leave it as-is for VS Code to resolve
        }

        // Set default values
        config.stopOnEntry = config.stopOnEntry || false;
        config.args = config.args || [];
        config.cwd = config.cwd || (folder ? folder.uri.fsPath : process.cwd());
        config.trace = config.trace || false;

        // Ensure mlpyPath is set
        if (!config.mlpyPath && folder) {
            config.mlpyPath = folder.uri.fsPath;
        }

        // Debug logging
        console.log('[ML Debug] config.program AFTER:', config.program);
        console.log('[ML Debug] config.mlpyPath:', config.mlpyPath);

        return config;
    }
}

/**
 * Register debug adapter and related functionality with VS Code.
 *
 * @param context Extension context
 */
export function registerDebugAdapter(context: vscode.ExtensionContext): void {
    console.log('[ML Debug] Registering debug adapter');

    // Register adapter factory
    const factory = new MLDebugAdapterDescriptorFactory();
    context.subscriptions.push(
        vscode.debug.registerDebugAdapterDescriptorFactory('ml', factory)
    );

    // Register debug configuration provider
    const provider = new MLDebugConfigurationProvider();
    context.subscriptions.push(
        vscode.debug.registerDebugConfigurationProvider('ml', provider)
    );

    // Show debug status messages
    context.subscriptions.push(
        vscode.debug.onDidStartDebugSession((session: vscode.DebugSession) => {
            if (session.type === 'ml') {
                console.log('[ML Debug] Debug session started:', session.name);
                const statusMessage = vscode.window.setStatusBarMessage(
                    '$(debug) ML Debugging...',
                    30000 // 30 seconds
                );
                context.subscriptions.push(statusMessage);
            }
        })
    );

    context.subscriptions.push(
        vscode.debug.onDidTerminateDebugSession((session: vscode.DebugSession) => {
            if (session.type === 'ml') {
                console.log('[ML Debug] Debug session ended:', session.name);
                vscode.window.setStatusBarMessage(
                    '$(check) ML Debug session ended',
                    5000 // 5 seconds
                );
            }
        })
    );

    // Register debug commands
    context.subscriptions.push(
        vscode.commands.registerCommand('ml.debug.startDebugging', async () => {
            const editor = vscode.window.activeTextEditor;

            if (!editor || editor.document.languageId !== 'ml') {
                vscode.window.showWarningMessage('Please open an ML file to start debugging');
                return;
            }

            // Start debugging with inline configuration
            await vscode.debug.startDebugging(undefined, {
                type: 'ml',
                request: 'launch',
                name: 'Debug Current File',
                program: editor.document.uri.fsPath,
                stopOnEntry: false
            });
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('ml.debug.startDebuggingWithEntry', async () => {
            const editor = vscode.window.activeTextEditor;

            if (!editor || editor.document.languageId !== 'ml') {
                vscode.window.showWarningMessage('Please open an ML file to start debugging');
                return;
            }

            // Start debugging with stop on entry
            await vscode.debug.startDebugging(undefined, {
                type: 'ml',
                request: 'launch',
                name: 'Debug Current File (Stop on Entry)',
                program: editor.document.uri.fsPath,
                stopOnEntry: true
            });
        })
    );

    console.log('[ML Debug] Debug adapter registered successfully');
}
