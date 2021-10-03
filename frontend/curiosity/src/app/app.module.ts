import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HomeComponent} from './home/home.component';
import {NavbarComponent} from './navbar/navbar.component';
import {LoginComponent} from './login/login.component';
import {RegisterComponent} from './register/register.component';
import {HttpClientModule} from '@angular/common/http'
import {HTTP_INTERCEPTORS} from '@angular/common/http';
import {TokenInterceptor} from './auth.interceptor';
import {AuthService} from './services/auth.service';
import {Router} from '@angular/router';
import {FormsModule} from "@angular/forms";
import {ActivateAccountComponent} from './activate-account/activate-account.component';
import {ProfileComponent} from './profile/profile.component';
import {PageNotFoundComponent} from './page-not-found/page-not-found.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatIconModule} from '@angular/material/icon';
import {MessageComponent} from './message/message.component';
import {PopupModule} from "./popup";
import {PasswordComponent} from './password/password.component';

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        NavbarComponent,
        LoginComponent,
        RegisterComponent,
        ActivateAccountComponent,
        ProfileComponent,
        PageNotFoundComponent,
        MessageComponent,
        PasswordComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        FormsModule,
        BrowserAnimationsModule,
        MatIconModule,
        PopupModule
    ],
    providers: [
        {
            provide: HTTP_INTERCEPTORS,
            useFactory: function (auth: AuthService, router: Router) {
                return new TokenInterceptor(auth, router);
            },
            deps: [AuthService, Router],
            multi: true
        }
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
