import PFAppRegistry from "@pfo/pf-react/src/artifacts/config/pf-app-registry";
import PFAppConfig from "@pfo/pf-react/src/artifacts/config/pf-app-config";
import PFURLMapping from "@pfo/pf-react/src/artifacts/config/pf-url-mapping";
import AppConfig from "./app-config";
import URLMapping from "./url-mapping";
import {PFAppContextProps} from "@pfo/pf-react/src/artifacts/config/pf-app-context";
import AuthConfig from "bl-identity-acl/app/view/auth/auth-config";
import AppContextProps from "./app-context-props";
import ModuleConfig from "../view/module-config";
import BLIdentityACLRegistry from "bl-identity-acl/app/bl-identity-acl-registry";


export default class AppRegistry extends PFAppRegistry {


    register(urlMapping: PFURLMapping, appConfig: PFAppConfig): void {
        AuthConfig.register(urlMapping, appConfig)
        ModuleConfig.register(urlMapping, appConfig)
        BLIdentityACLRegistry.register(urlMapping, appConfig)
    }

    initContextProps(): PFAppContextProps | undefined {
        return new AppContextProps();
    }

    initAppConfig(): PFAppConfig {
        return new AppConfig();
    }

    initURLMapping(): PFURLMapping {
        return new URLMapping()
    }

}