import React from 'react';
import CoreUIConfig from "@bl/core-ui/bl/core-ui/config/core-ui-config";
import PFHTTResponse from "@pfo/pf-react/src/artifacts/processor/http/pf-http-response";
import PFHTTAuthCallback from "@pfo/pf-react/src/artifacts/processor/http/pf-http-auth-callback";
import PFHTTRequest from "@pfo/pf-react/src/artifacts/processor/http/pf-http-request";
import {PFHTTPCall} from "@pfo/pf-react/src/artifacts/interface/pf-mixed-interface";
import AuthenticationService from "bl-identity-acl/app/service/authentication-service";

export default class AppConfig extends CoreUIConfig {

    public staticURL: string = process.env["STATIC_URL"] || "http://127.0.0.1:1511/";

    public getBaseURL(): string {
        return process.env["BASE_URL"] || "http://127.0.0.1:1511/";
    }

    public isAuthorized(response?: PFHTTResponse): boolean {
        if (response && response.httpCode === 401) {
            return false
        }
        return true;
    }

    public authCallback(): PFHTTAuthCallback | undefined {
        let authCallback: PFHTTAuthCallback = {
            process(request: PFHTTRequest): PFHTTRequest {
                return AuthenticationService.instance().processAuth(request);
            }
        };
        return authCallback;
    }

    public renewAuthorization(trHttpCall: PFHTTPCall): void {
        AuthenticationService.instance().renewAuthorization(trHttpCall);
    }

}