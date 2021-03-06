import {Component, ElementRef, OnInit} from '@angular/core';
import {Observable} from "rxjs";
import {AuthService} from "../services/auth.service";
import {NavService} from "../services/nav.service";
import {Profile} from "../interfaces";
import {Router} from "@angular/router";

@Component({
    selector: 'app-navbar',
    templateUrl: './navbar.component.html',
    styleUrls: ['./navbar.component.scss'],
    host: {
        '(document:click)': 'closeOnOutsideClick($event)',
    },
})
export class NavbarComponent implements OnInit {

    showNav: Observable<boolean>;
    showDropdown: Observable<boolean>;
    isLoggedIn: Observable<boolean>;
    profile: Observable<Profile>;
    name = "";
    picUrl = "";

    constructor(private router: Router, private auth: AuthService,
                private nav: NavService, private _eref: ElementRef) {
        this.showNav = nav.getShowNav();
        this.showDropdown = nav.getShowDropdown();
        this.isLoggedIn = auth.isLoggedIn();
        this.profile = auth.getProfile();
        this.profile.subscribe({
            next: value => {
                this.name = value?.user.first_name;
                this.picUrl = value?.profile_pic;
            }
        });
        nav.getShowNav().subscribe(
            show => {
                if (show) document.body.style.overflowY = "hidden";
                else document.body.style.overflowY = "scroll";
            }
        )
    }

    ngOnInit(): void {
    }

    toggleMenu() {
        this.nav.toggleNav();
    }

    logout() {
        this.auth.logout();
    }

    toggleDropDown() {
        this.nav.toggleDropdown();
    }

    closeOnOutsideClick(event: any) {
        if (!this._eref.nativeElement.querySelector('#acc-view')?.contains(event.target)) // or some similar check
            this.nav.showDropdown(false);
    }
}
