import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";
import { NgModule } from '@angular/core';

import { AppComponent } from './components/app.component';
import { PackMaster } from "./components/packmaster.component";
import { PackList } from "./components/packlist.component";

@NgModule({
  declarations: [
    AppComponent,
    PackMaster,
    PackList
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
