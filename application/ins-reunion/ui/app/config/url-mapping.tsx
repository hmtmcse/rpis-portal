import React from 'react';
import PFURLMapping from "@pfo/pf-react/src/artifacts/config/pf-url-mapping";
import PFLayoutInfoData from "@pfo/pf-react/src/artifacts/data/pf-layout-info-data";
import AuthLayout from "@bl/core-ui/bl/core-ui/layout/auth-layout";
import PrivateLayout from "@bl/core-ui/bl/core-ui/layout/private-layout";
import PublicLayout from "@bl/core-ui/bl/core-ui/layout/public-layout";



export default class URLMapping extends PFURLMapping {

    public getLayoutsAndPages(): Array<PFLayoutInfoData> {
        let pageWithLayout: Array<PFLayoutInfoData> = [];
        this.publicLayout.layout = PublicLayout
        this.privateLayout.layout = PrivateLayout
        this.authLayout.layout = AuthLayout

        pageWithLayout.push(this.publicLayout);
        pageWithLayout.push(this.privateLayout);
        pageWithLayout.push(this.authLayout);
        return pageWithLayout
    }

}