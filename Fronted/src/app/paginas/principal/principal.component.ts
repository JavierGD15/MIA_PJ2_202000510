import { Component, Input, OnInit } from '@angular/core';
import { UserInteractionService } from 'src/app/services/index';
import { Analisis } from 'src/app/models/analisis';
import { AnalisisService } from 'src/app/services/analisis.service';
import 'codemirror/mode/go/go';
import 'codemirror/mode/julia/julia';
import 'codemirror/mode/markdown/markdown';
import * as Models from 'src/app/models/models';
import { Router } from '@angular/router';
import { TabPanel } from 'src/app/models/models';
import { graphviz } from 'd3-graphviz';

@Component({
  selector: 'app-principal',
  templateUrl: './principal.component.html',
  styleUrls: ['./principal.component.scss'],
})
export class PrincipalComponent implements OnInit {
  template: Array<Models.TabPanel> = [];
  c: number = 1;
  tabContent: string = 'Tab 0';
  content = [];
  number = [];
  contenido: TabPanel = new TabPanel('');
  salida = '';
  optimizado = '';
  grafo: string;
  tablaSimbolos: string;
  errores: string;
  data = [];
  mostrar_errores = false;

  text: Analisis = {
    entrada: '',
  };

  constructor(
    private userInteractionService: UserInteractionService,
    private analizador: AnalisisService
  ) {}

  ngOnInit() {
    this.template = [];
    this.c = 0;
    this.tabContent = 'Tab 0';
    this.addTab();
    this.contenido = this.template[0];
    this.tabContent = this.template[0].name;
  }

  addTab() {
    if (this.template.length == 0) {
      this.c = 0;
      this.number.push(this.c);
    }
    var tmp = 'Tab ' + String(this.c);
    var tab: Models.TabPanel = new Models.TabPanel(tmp);
    this.content.push('//Nuevo tab ' + this.c);
    this.number.push(this.c);
    this.c += 1;
    this.template.push(tab);
  }

  interpretar() {
    this.text.entrada = this.contenido.content;
    console.log(this.text);
    this.analizador.interpretar(this.text).subscribe(
      (res) => {
        console.log(res);
        this.salida = res.salida;
        this.grafo = res.dot;
        this.tablaSimbolos = res.tabladot;
        this.errores = res.doterrores;
      },
      (err) => {
        console.log(err);
      }
    );
  }

  optimizar() {
    this.text.entrada = this.salida;
    this.analizador.optimizar(this.text).subscribe((res) => {
      this.optimizado = res.salida;
      this.data = res.optimizaciones;
    });
  }

  cargarArchivo() {}

  async upload(e: any) {
    let files = e.srcElement.files;
    let currnt = files[0];
    let input = e.target;
    let reader = new FileReader();
    reader.readAsText(input.files[0]);

    reader.onload = async () => {
      let tyData = <string>reader.result;
      this.contenido.content = tyData;
    };
  }

  saveAsProject() {
    this.writeContents(
      this.contenido.content,
      this.contenido.name + '.ty',
      'text/plain'
    );
  }
  writeContents(content, fileName, contentType) {
    var a = document.createElement('a');
    var file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
  }

  graficar() {
    graphviz('#graphTable').renderDot(this.grafo);
  }

  graficarTablaSimbolos() {
    graphviz('#graphTable').renderDot(this.tablaSimbolos);
  }

  graficarErrores() {
    graphviz('#graphTable').renderDot(this.errores);
  }

  async removeTab() {
    if (this.template.length == 0) {
      await this.userInteractionService.notify('No hay tabs para remover');
      return;
    }
    var ok = await this.userInteractionService.confirmAction(
      'Sera eliminado el tab ' + this.tabContent + '¿Esta seguro?'
    );
    if (!ok) {
      return;
    }
    this.template = this.template.filter((obj) => {
      return obj.name != this.tabContent;
    });
  }

  async refresh() {
    var ok = await this.userInteractionService.confirmAction(
      'Se refrescara la pagina'
    );
    if (!ok) {
      return;
    }
    this.ngOnInit();
  }

  toolbarItems: Array<any> = [
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'plus',
        hint: 'Añadir tab',
        stylingMode: 'contained',
        onClick: this.addTab.bind(this),
      },
    },
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'remove',
        hint: 'Eliminar tab',
        stylingMode: 'contained',
        onClick: this.removeTab.bind(this),
      },
    },
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'codeblock',
        hint: 'Compilar',
        stylingMode: 'contained',
        onClick: this.interpretar.bind(this),
      },
    },
    {
      location: 'left',
      widget: 'dxButton',
      options: {
        icon: 'save',
        hint: 'Guardar',
        stylingMode: 'contained',
        onClick: this.saveAsProject.bind(this),
      },
    },
    {
      location: 'left',
      widget: 'dxButton',
      options: {
        icon: 'upload',
        hint: 'Cargar Archivo',
        stylingMode: 'contained',
        onClick: this.interpretar.bind(this),
      },
    },
  ];

  selectTab(e: any) {
    this.tabContent = e.addedItems[0].name;
    this.contenido = e.addedItems[0];
  }
}
