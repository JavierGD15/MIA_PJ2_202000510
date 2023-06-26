import { Injectable, Output } from "@angular/core";
import { BehaviorSubject } from "rxjs";
import {
  custom as customDialogComponent,
  alert as alertComponent,
} from "devextreme/ui/dialog";


@Injectable({
  providedIn: "root",
})
export class UserInteractionService {
  @Output() appLoadingChange: BehaviorSubject<boolean> = new BehaviorSubject<
    boolean
  >(false);

  constructor() {}

  async notify(errorObject: any, title?: string) {
    try {
      let errorMessage =
        typeof errorObject === "object"
          ? errorObject.error || errorObject.message
            ? errorObject.message || errorObject.error
            : JSON.stringify(errorObject)
          : errorObject;

      let customDialog = customDialogComponent({
        title: title ? title : "¡Lo sentimos!",
        messageHtml: `<i>${errorMessage}</i>`,
        buttons: [
          {
            text: "Aceptar",
            onClick: () => {
              errorMessage = null;
              customDialog = null;
            },
          },
        ],
      });

   
      return await customDialog.show();
    } catch (error) {
      return Promise.resolve();
    }
  }

  alert(message: string, title: string): Promise<void> {

    return alertComponent(`<i>${message}</i>`, title);
  }

  async confirmAction(message: string, title?: string): Promise<boolean> {
    try {
      const customDialog = customDialogComponent({
        title: title ? title : "Atención",
        messageHtml: `<i>${message}</i>`,
        buttons: [
          {
            text: "Si",
            onClick: () => {
              return Promise.resolve(true);
            },
          },
          {
            text: "No",
            onClick: () => {
              return Promise.resolve(false);
            },
          },
        ],
      });

      const result = await customDialog.show();

      return Promise.resolve(result);
    } catch (error) {
      return Promise.resolve(false);
    }
  }

  async showErrorList(
    errorListHtmlString: string,
    title?: string
  ): Promise<void> {
    let customDialog = customDialogComponent({
      title: title ? title : "¡Lo sentimos!",
      messageHtml: errorListHtmlString,
      buttons: [
        {
          text: "Aceptar",
          onClick: (_e) => {
            customDialog = null;
          },
        },
      ],
    });

    await customDialog.show();
  }
}
