import * as vscode from 'vscode';
import got from 'got';

const oasisUrl = "https://0.0.0.0:9000";


interface oasisResponse {
	response: EditResponse;
}

interface EditResponse {
	text: string;
	index: number;
}

async function useoasis(command: string) {
	const activeEditor = vscode.window.activeTextEditor;
	if (!activeEditor) {
		return;
	}

	const document = activeEditor.document;
	const selection = activeEditor.selection;

	const text = document.getText(selection);

	const requestBody = JSON.stringify({
		data: text
	});
	const url = `${oasisUrl}/${command}`;

	console.log("Calling API", url, "with body: ", requestBody);

	let response: oasisResponse | undefined = undefined;
	try {
		response = await got(url, {
			method: "POST",
			headers: {
				// eslint-disable-next-line @typescript-eslint/naming-convention
				"Content-Type": "application/json",
				// eslint-disable-next-line @typescript-eslint/naming-convention
			},
			body: requestBody
		}).json();
	} catch (e: any) {
		vscode.window.showErrorMessage("Oasis Plugin: error calling the API")
		try {
			const apiStatusCode = `Error calling API: ${e.response.statusCode}`;
			vscode.window.showErrorMessage(apiStatusCode);
		} catch (error) {
			console.error("Error parsing error response code", error);
		}
	}

	if (response) {
		console.log("From got", response);
		const editedText = response.response.text;

		activeEditor.edit(editBuilder => {
			console.log("Edit builder", editBuilder);
			editBuilder.replace(selection, editedText);
		});
	}


};

export function activate(context: vscode.ExtensionContext) {
	const commands = [
		["addDocstring", "add_docstring"],
		["addTypeHints", "add_type_hints"],
		["addUnitTest", "add_unit_test"],
		["fixSyntaxError", "fix_syntax_error"],
		["improveCodeQuality", "improve_code_quality"],
	];
	commands.forEach(tuple_ => {
		const [commandName, oasisCommand] = tuple_;
		const command = vscode.commands.registerCommand(`oasis.${commandName}`, () => {
			useoasis(oasisCommand);
		});
		context.subscriptions.push(command);
	});
}

// this method is called when your extension is deactivated
export function deactivate() {
	console.log("deactivated");
}
